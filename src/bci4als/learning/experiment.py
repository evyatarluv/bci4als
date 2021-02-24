from brainflow import BrainFlowInputParams, BoardShim, BoardIds
from psychopy import event


class Experiment:

    def __init__(self, eeg, num_trials):
        self.eeg = eeg
        self.num_trials = num_trials

    def run(self):
        pass


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

