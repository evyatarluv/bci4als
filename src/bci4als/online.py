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
from psychopy import visual, core
from sklearn.linear_model import SGDClassifier
import os


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
                 buffer_time: float, threshold: int, num_labels: int = 5):

        super().__init__(eeg, num_trials)
        self.threshold: int = threshold
        self.buffer_time: float = buffer_time
        self.model = model
        self.win = None
        self.num_labels = num_labels
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

            # Get the data
            features = self.eeg.get_features(channels=['C3', 'C4'], low_pass=8, high_pass=30,
                                             selected_funcs=['pow_freq_bands', 'variance'])

            # Reset the clock for the next buffer
            timer.reset()

            # Predict using the subject EEG data
            prediction = self.model.predict(features)[0]
            prediction = {1: 2, 2: 1, 3: 0}[prediction]  # translate the model prediction to the Feedback prediction
            # conf_predict = self.model.decision_function(features)

            # Update the feedback according the prediction
            feedback.update(prediction)
            # feedback.update(stim)  # debug

            # Update the model using partial-fit with the new EEG data
            # self.model.partial_fit(features, [stim])

            # Debug
            print('Predict: {}, True: {}'.format(prediction, stim))

    def warmup(self, use_eeg: bool = True, target: str = 'right'):

        # matplotlib config
        matplotlib.use('TkAgg')
        fig, ax = plt.subplots(1, 2)

        # Turn on the EEG streaming
        if use_eeg:
            self.eeg.on()

        # Define the animation function
        target_num = {'idle': 1, 'left': 2, 'right': 3}[target]
        correct, total = 0, 0

        def animate(i, buffer, eeg, model, target_num):

            nonlocal correct, total, target

            # Wait for the buffer to fill up
            time.sleep(buffer)

            # Extract features from collected data
            features = eeg.get_features(channels=['C3', 'C4'], low_pass=8, high_pass=30,
                                        selected_funcs=['pow_freq_bands', 'variance'])
            # features = np.random.rand(1, 8)  # debug

            # Predict using the subject EEG data
            conf_predict = model.decision_function(features)[0]
            # probs = np.exp(conf_predict)/np.sum(np.exp(conf_predict))
            prediction = model.predict(features)[0]

            # Plot confidence bar plot
            ax[0].clear()
            ax[0].bar(['Idle', 'Left', 'Right'], conf_predict, color='lightblue')
            ax[0].set_title('Classification Probabilities')
            ax[0].set_ylim(-20, 20)

            # Plot miss classifications
            if prediction == target_num:
                correct += 1
            total += 1
            ax[1].clear()
            ax[1].bar(['Accuracy'], correct / total, color='limegreen')
            ax[1].set_title('Accuracy: Predict = {}'.format(target.capitalize()))
            ax[1].set_ylim(0, 1)

        # Start Animation
        ani = FuncAnimation(fig, animate,
                            fargs=(self.buffer_time, self.eeg, self.model, target_num), interval=10)
        plt.show()

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
