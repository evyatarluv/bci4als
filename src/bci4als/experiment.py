import os

from bci4als.eeg import EEG
from bci4als.feedback import Feedback
from psychopy import event


class Experiment:

    def __init__(self, eeg, num_trials):
        self.eeg: EEG = eeg
        self.num_trials: int = num_trials

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
            eeg.clear_board()

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

    @staticmethod
    def create_session_folder(subject_folder: str) -> str:
        """
        The method create new folder for the current session. The folder will be at the given subject
        folder.
        The method also creating a metadata file and locate it inside the session folder
        :param subject_folder: path to the subject folder
        :return: session folder path
        """

        current_sessions = []
        for f in os.listdir(subject_folder):

            # try to convert the current sessions folder to int
            # and except if one of the sessions folder is not integer
            try:
                current_sessions.append(int(f))

            except ValueError:
                continue

        # Create the new session folder
        session = (max(current_sessions) + 1) if len(current_sessions) > 0 else 1
        session_folder = os.path.join(subject_folder, str(session))
        os.mkdir(session_folder)

        return session_folder

