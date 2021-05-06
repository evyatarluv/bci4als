import random
import threading
import time
import matplotlib
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from typing import Dict, List
from bci4als.eeg import EEG
from bci4als.experiment import Experiment
from bci4als.feedback import Feedback
from bci4als.dashboard import Dashboard
from psychopy import visual, core
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import SGDClassifier
from mne_features.feature_extraction import extract_features
import mne
from nptyping import NDArray
import os

from sklearn.preprocessing import StandardScaler


class OnlineExperiment(Experiment):
    """
    Class for running an online MI experiment.

    Attributes:
    ----------

        num_trials (int):
            Amount of trials in the experiment.

        buffer_time (float):
            Time in seconds for collecting EEG data before model's prediction.

        threshold (int):
            The amount the times the model need to be correct (predict = stim) before moving to the next stim.

    """

    def __init__(self, eeg: EEG, model: SGDClassifier, num_trials: int,
                 buffer_time: float, threshold: int):

        super().__init__(eeg, num_trials)
        self.threshold: int = threshold
        self.buffer_time: float = buffer_time
        self.model = model
        self.win = None

        # Model configs
        self.labels_enum: Dict[str, int] = {'right': 0, 'left': 1, 'idle': 2, 'tongue': 3, 'legs': 4}
        self.num_labels: int = len(self.labels_enum)

        # Init trials for the experiment
        self.trials = self._init_trials()

    def _init_trials(self) -> List[int]:
        """
        Create list with trials as num_trials attributes.
        The trials consists of equal number of right and left targets (0, 1).
        :return:
        """
        trials = []
        # Create the balance label vector
        for i in range(self.num_labels):
            trials += [i] * (self.num_trials // self.num_labels)
        trials += list(np.random.choice(np.arange(self.num_labels),
                                        size=self.num_trials % self.num_labels,
                                        replace=True))
        random.shuffle(trials)

        # Save the labels as csv file
        # pd.DataFrame.from_dict({'name': self.labels}).to_csv(os.path.join(self.subject_directory, 'labels.csv'),
        #                                                      index=False, header=False)
        return trials

    def _learning_model(self, feedback: Feedback, stim: int):

        """
        The method for learning the model from the current stim.

        A separate thread runs this method. The method responsible for the following steps:
            1. Collecting the EEG data from the board (according to the buffer time attribute).
            2. Predicting the stim using the current model and collected EEG data.
            3. Updating the feedback object according to the model's prediction.
            4. Updating the model according to the data and stim.

        :param feedback: feedback visualization for the subject
        :param stim: current stim
        :return:
        """

        timer = core.Clock()

        while not feedback.confident:
            # Sleep until the buffer full
            time.sleep(max(0, self.buffer_time - timer.getTime()))

            # Extract features from the EEG data
            data = self.eeg.get_channels_data()
            # data = np.random.rand(13, 125 * 4)  # debug
            x = self.online_pipe(data)

            # Reset the clock for the next buffer
            timer.reset()

            # Predict using the subject EEG data
            prediction = self.model.predict([x])[0]
            # conf_predict = self.model.decision_function(features)

            # Update the feedback according the prediction
            feedback.update(prediction)
            # feedback.update(stim)  # debug

            # Update the model using partial-fit with the new EEG data
            # self.model.partial_fit([x], [stim])

            # Debug
            print(f'Predict: {prediction}, True: {stim}')

    def warmup(self, use_eeg: bool = True, target: str = 'right'):

        # matplotlib config
        matplotlib.use('TkAgg')
        fig, ax = plt.subplots(1, 2)

        # Turn on the EEG streaming
        if use_eeg:
            self.eeg.on()

        # Define the animation function
        target_num = self.labels_enum[target]
        correct, total = 0, 0
        timer = core.Clock()

        def animate(i: int, exp: OnlineExperiment, dash: Dashboard):

            nonlocal correct, total, target, timer

            # Wait for the buffer to fill up
            time.sleep(max(0, exp.buffer_time - timer.getTime()))

            # Get features from the current EEG data
            data = exp.eeg.get_channels_data()
            # data = np.random.rand(16, 125 * 4)  # debug
            x = exp.online_pipe(data)
            # x = Nystroem(kernel='rbf', gamma=1/8).fit_transform(x.reshape(1,-1))  # test transform

            # Reset the timer for the next round
            timer.reset()

            # Predict using the model
            confidence = exp.model.decision_function([x])[0]
            prediction = exp.model.predict([x])[0]

            # Plots
            # Confidence plot
            ax[0] = dash.confidence_plot(ax[0], list(exp.labels_enum.keys()), confidence)

            # Accuracy
            if prediction == target_num:
                correct += 1
            total += 1
            ax[1] = dash.accuracy_plot(ax[1], correct / total, target.capitalize())

        # Start Animation
        ani = FuncAnimation(fig, animate,
                            fargs=(self, Dashboard()),
                            interval=10)
        plt.show()

    def online_pipe(self, data: NDArray) -> NDArray:
        """
        The method get the data as ndarray with dimensions of (n_channels, n_samples).
        The method returns the features for the given data.
        :param data: ndarray with the shape (n_channels, n_samples)
        :return: ndarray with the shape of (1, n_features)
        """
        # Prepare the data to MNE functions
        data = data.astype(np.float64)

        # Filter the data (band-pass only)
        data = mne.filter.filter_data(data, l_freq=8, h_freq=30, sfreq=self.eeg.sfreq, verbose=False)

        # Laplacian
        data = self.eeg.laplacian(data, self.eeg.get_board_names())

        # Normalize
        scaler = StandardScaler()
        data = scaler.fit_transform(data.T).T

        # Extract features
        funcs_params = {'pow_freq_bands__freq_bands': np.array([8, 10, 12.5, 30])}
        selected_funcs = ['pow_freq_bands', 'variance']
        X = extract_features(data[np.newaxis], self.eeg.sfreq, selected_funcs, funcs_params)[0]

        return X

    def run(self, use_eeg: bool = True, full_screen: bool = False):

        # Init experiments configurations
        self.win = visual.Window(monitor='testMonitor', fullscr=full_screen)

        # turn on EEG streaming
        if use_eeg:
            self.eeg.on()

        # For each stim in the trials list
        for stim in self.trials:

            # Init feedback instance
            feedback = Feedback(self.win, stim, self.buffer_time, self.threshold)

            # Use different thread for online learning of the model
            threading.Thread(target=self._learning_model, args=(feedback, stim)).start()

            # Maintain visual feedback on screen
            timer = core.Clock()

            while not feedback.confident:

                feedback.display(current_time=timer.getTime())

                # Reset the timer according the buffer time attribute
                if timer.getTime() > self.buffer_time:
                    timer.reset()

            # Waiting for key-press between trials
            self._wait_between_trials(feedback, self.eeg, use_eeg)

        # turn off EEG streaming
        if use_eeg:
            self.eeg.off()
