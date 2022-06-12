import os
import random
import sys
from datetime import datetime
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter import Tk, Entry, Label, Button

import brainflow
import numpy as np

from bci4als.eeg import EEG
from bci4als.experiments.feedback import Feedback
from psychopy import event


class Experiment:
    def __init__(self, eeg, num_trials):
        self.num_trials: int = num_trials
        self.eeg: EEG = eeg

        if self.eeg.board_id == brainflow.BoardIds.SYNTHETIC_BOARD:
            messagebox.showwarning(title="bci4als WARNING", message="You are running a synthetic board!")
            self.debug = True
        else:
            self.debug = False
        # override in subclass
        self.cue_length = None
        self.trial_length = None
        self.session_directory = None
        self.enum_image = {0: 'right', 1: 'left', 2: 'idle', 3: 'tongue', 4: 'legs'}
        self.experiment_type = None
        self.skip_after = None

        #     labels
        self.labels = []
        self._init_labels()

    def run(self):
        pass

    def write_metadata(self):
        # The path of the metadata file
        path = os.path.join(self.session_directory, 'metadata.txt')

        with open(path, 'w') as file:
            # Datetime
            file.write(f'Experiment datetime: {datetime.now()}\n\n')

            # Channels
            file.write('EEG Channels:\n')
            file.write('*************\n')
            for index, ch in enumerate(self.eeg.get_board_names()):
                file.write(f'Channel {index + 1}: {ch}\n')

            # Experiment data
            file.write('\nExperiment Data\n')
            file.write('***************\n')
            file.write(f'Experiment Type: {self.experiment_type}\n')
            file.write(f'Num of trials: {self.num_trials}\n')
            file.write(f'Trials length: {self.trial_length}\n')
            file.write(f'Cue length: {self.cue_length}\n')
            file.write(f'Labels Enum: {self.enum_image}\n')
            file.write(f'Skip After: {self.skip_after}\n')

    def _ask_subject_directory(self):
        """
        init the current subject directory
        :return: the subject directory
        """

        # get the CurrentStudy recording directory
        if not messagebox.askokcancel(title='bci4als',
                                      message="Welcome to the motor imagery EEG recorder."
                                              "\n\nNumber of trials: {}\n\n"
                                              "Please select the subject directory:".format(self.num_trials)):
            sys.exit(-1)

        # show an "Open" dialog box and return the path to the selected file
        init_dir = os.path.join(os.path.split(os.path.abspath(''))[0], 'recordings')
        subject_folder = askdirectory(initialdir=init_dir)
        if not subject_folder:
            sys.exit(-1)
        return subject_folder

    def ask_num_trials(self):
        win = Tk()
        win.geometry('400x300')

        # Define a function to return the Input data
        def get_num_trials():
            try:
                self.num_trials = entry.get()
            except:
                ValueError('You should enter a number!')
            win.destroy()

        entry = Entry(win, width=42)
        entry.place(relx=.5, rely=.2, anchor='center')
        label = Label(win, text="Enter the number of trials you want.", font=('Helvetica 13'))
        label.pack()
        Button(win, text="submit", command=get_num_trials).place(relx=.5, rely=.3)
        win.mainloop()

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

    def _init_labels(self, keys=(0, 1, 2, 3, 4)):
        """
        This method creates dict containing a stimulus vector
        :return: the stimulus in each trial (list)
        """

        # keys = [3, 4] #todo: make the list of keys programmable from main scope (run experiment with limited keys)
        # Create the balance label vector
        for i in keys:
            self.labels += [i] * (self.num_trials // len(keys))
        self.labels += list(np.random.choice(list(keys),
                                             size=self.num_trials % len(keys),
                                             replace=True))

        random.shuffle(self.labels)



