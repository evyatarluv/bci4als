import json
import os
import pickle
import random
import sys
import threading
import time
from typing import Dict, Union
import matplotlib
import matplotlib.pyplot as plt
import mne
import numpy as np
import playsound
from bci4als.eeg import EEG
from .experiment import Experiment
from bci4als.experiments.feedback import Feedback
from bci4als.ml_model import MLModel
from matplotlib.animation import FuncAnimation
from mne_features.feature_extraction import extract_features
from nptyping import NDArray
from psychopy import visual, core
from sklearn.preprocessing import StandardScaler

from .feedback_unity import FeedbackUnity


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

    def __init__(self, eeg: EEG, model: MLModel, num_trials: int,
                 buffer_time: float, threshold: int, skip_after: Union[bool, int] = False,
                 co_learning: bool = False, debug=False):

        super().__init__(eeg, num_trials)
        # experiment params
        self.experiment_type = "Online"
        self.threshold: int = threshold
        self.buffer_time: float = buffer_time
        self.model = model
        self.skip_after = skip_after
        # self.debug = self.model.debug
        self.debug = debug
        self.co_learning: bool = co_learning

        # audio
        # self.audio_success_path = os.path.join(os.path.dirname(__file__), 'audio', f'success.mp3')
        self.audio_success_path = r'C:\Users\noam\PycharmProjects\bci_4_als\src\bci4als\audio\success.mp3'
        # todo: make this path generic

        # Model configs
        self.labels_enum: Dict[str, int] = {'right': 0, 'left': 1, 'idle': 2, 'tongue': 3, 'legs': 4}
        self.label_dict: Dict[int, str] = dict([(value, key) for key, value in self.labels_enum.items()])
        self.num_labels: int = len(self.labels_enum)

        # Hold list of lists of target-prediction pairs per trial
        # Example: [ [(0, 2), (0,3), (0,0), (0,0), (0,0) ] , [ ...] , ... ,[] ]
        self.results = []

    def _learning_model(self, feedback: FeedbackUnity, stim: int):

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
        target_predictions = []
        num_tries = 0
        while not feedback.stop:
            # increase num_tries by 1
            print(f"num tries {num_tries}")

            # Sleep until the buffer full
            time.sleep(max(0, self.buffer_time - timer.getTime()))

            # Extract features from the EEG data
            data = self.eeg.get_channels_data()

            # Predict the class
            if self.debug:
                # in debug mode, be correct 2/3 of the time and incorrect 1/3 of the time.
                prediction = stim if np.random.rand() <= 2 / 3 else (stim + 1) % len(self.labels_enum)
            else:
                # in normal mode, use the loaded model to make a prediction
                prediction, confidence = self.model.online_predict(data, eeg=self.eeg, return_confidence=True)
                # predict_confidence = self.model.clf.steps[1][1].predict_proba(data)

            # play sound if successful
            # todo: make this available to object params
            self.play_sound = False
            if self.play_sound:
                if prediction == stim:
                    playsound.playsound(self.audio_success_path)

            # if self.co_learning and (prediction == stim):
            if self.co_learning:
                self.model.partial_fit(self.eeg, data, stim)
                pickle.dump(self.model, open(os.path.join(self.session_directory, 'model.pickle'), 'wb'))

            target_predictions.append((int(stim), int(prediction)))

            # Reset the clock for the next buffer
            timer.reset()

            if stim == prediction:
                num_tries = 0  # if successful, reset num_tries to 0
            else:
                num_tries += 1

            # Update the feedback according the prediction
            feedback.update(prediction, confidence, skip=True)
            # feedback.update(stim)  # For debugging purposes

            # Update the model using partial-fit with the new EEG data
            # self.model.partial_fit([x], [stim])  # todo: implement this with csp_lda

            # Debug
            print(f'Predict: {self.label_dict[prediction]}; '
                  f'True: {self.label_dict[stim]}')
        accuracy = sum([1 if p[1] == p[0] else 0 for p in target_predictions]) / len(target_predictions)
        print(f'Accuracy of last target: {accuracy}')
        self.results.append(target_predictions)

        # Save Results
        json.dump(self.results, open(os.path.join(self.session_directory, 'results.json'), "w"))

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

        # Init the current experiment folder
        self.subject_directory = self._ask_subject_directory()
        self.session_directory = self.create_session_folder(self.subject_directory)

        # Create experiment's metadata
        self.write_metadata()

        # turn on EEG streaming
        if use_eeg:
            self.eeg.on()

        # Init feedback instance
        feedback = FeedbackUnity(buffer_time=self.buffer_time, threshold=self.threshold)

        # For each stim in the trials list
        for stim in self.labels:

            # Init feedback stimulation
            feedback.set_stimulation(stim)

            # Use different thread for online learning of the model
            threading.Thread(target=self._learning_model,
                             args=(feedback, stim), daemon=True).start()

            # Maintain visual feedback on screen
            timer = core.Clock()

            while not feedback.stop:

                feedback.display(current_time=timer.getTime())

                # Reset the timer according the buffer time attribute
                if timer.getTime() > self.buffer_time:
                    timer.reset()

                # Halt if escape was pressed
                if 'escape' == self.get_keypress():
                    sys.exit(-1)

            # Waiting for key-press between trials
            self._wait_between_trials(feedback, self.eeg, use_eeg)

        feedback.close()

        # turn off EEG streaming
        if use_eeg:
            self.eeg.off()
