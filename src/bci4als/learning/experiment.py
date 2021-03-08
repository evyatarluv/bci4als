from bci4als.learning.eeg import EEG
from bci4als.learning.online import Feedback
from brainflow import BrainFlowInputParams, BoardShim, BoardIds
from psychopy import event


class Experiment:

    def __init__(self, eeg, num_trials):
        self.eeg = eeg
        self.num_trials = num_trials

    def run(self):
        pass

    @staticmethod
    def _wait_between_trials(feedback: Feedback, eeg: EEG, use_eeg: bool):
        """
        Method for waiting between trials.

        1. Show and empty feedback while waiting.
        2. wait for user's key-press
        3. Empty the EEG board
        """

        # Show empty feedback
        feedback.display(0)

        # Wait for key-press
        event.waitKeys()

        # Empty the board
        if use_eeg:
            eeg.get_data()

    @staticmethod
    def get_keypress():
        """
        Get keypress of the user
        :return: string of the key
        """

        keys = event.getKeys()
        if keys:
            return keys[0]
        else:
            return None

