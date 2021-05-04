import datetime
import os
import pickle
import random
import sys
import time
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askdirectory
from typing import Dict, List, Any
import numpy as np
import pandas as pd
from bci4als.experiment import Experiment
from bci4als.eeg import EEG
from psychopy import visual


class OfflineExperiment(Experiment):

    def __init__(self, eeg: EEG, num_trials: int, trial_length: float,
                 next_length: float = 1, cue_length: float = 0.25, ready_length: float = 1, full_screen=False):

        super().__init__(eeg, num_trials)
        self.subject_directory: str = ''
        self.window_params: Dict[str, Any] = {}
        self.labels: List[int] = []
        self.full_screen = full_screen

        # trial times
        self.cue_length: float = cue_length
        self.next_length: float = next_length
        self.ready_length: float = ready_length
        self.trial_length: float = trial_length

        # paths
        self.images_path: Dict[str, str] = {
            'right': os.path.join(os.path.dirname(__file__), 'images', 'arrow_right.jpeg'),
            'left': os.path.join(os.path.dirname(__file__), 'images', 'arrow_left.jpeg'),
            'idle': os.path.join(os.path.dirname(__file__), 'images', 'square.jpeg'),
            'tongue': os.path.join(os.path.dirname(__file__), 'images', 'tongue.jpeg'),
            'legs': os.path.join(os.path.dirname(__file__), 'images', 'legs.jpeg')}
        self.enum_image = {0: 'right', 1: 'left', 2: 'idle', 3: 'tongue', 4: 'legs'}
        self.visual_params: Dict[str, Any] = {'text_color': 'white', 'text_height': 48}

    def _init_directory(self):
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
        recording_folder = askdirectory(initialdir=init_dir)
        if not recording_folder:
            sys.exit(-1)

        # Init the current experiment folder
        self.subject_directory = self.create_session_folder(recording_folder)

        # Create experiment's metadata
        self.create_metadata()

    def create_metadata(self):

        # The path of the metadata file
        path = os.path.join(self.subject_directory, 'metadata.txt')

        with open(path, 'w') as file:

            # Datetime
            file.write(f'Experiment datetime: {datetime.datetime.now()}\n\n')

            # Channels
            file.write('EEG Channels:\n')
            file.write('*************\n')
            for index, ch in enumerate(self.eeg.get_board_names()):
                file.write(f'Channel {index}: {ch}\n')

            # Experiment data
            file.write('\nExperiment Data\n')
            file.write('***************\n')
            file.write(f'Num of trials: {self.num_trials}\n')
            file.write(f'Trials length: {self.trial_length}\n')
            file.write(f'Cue length: {self.cue_length}\n')
            file.write(f'Labels Enum: {self.enum_image}\n')

    def _init_window(self):
        """
        init the psychopy window
        :return: dictionary with the window, left arrow, right arrow and idle.
        """

        # Create the main window
        main_window = visual.Window(monitor='testMonitor', units='pix', color='black', fullscr=self.full_screen)

        # Create right, left and idle stimulus
        right_stim = visual.ImageStim(main_window, image=self.images_path['right'])
        left_stim = visual.ImageStim(main_window, image=self.images_path['left'])
        idle_stim = visual.ImageStim(main_window, image=self.images_path['idle'])
        tongue_stim = visual.ImageStim(main_window, image=self.images_path['tongue'])
        legs_stim = visual.ImageStim(main_window, image=self.images_path['legs'])

        self.window_params = {'main_window': main_window, 'right': right_stim, 'left': left_stim,
                              'idle': idle_stim, 'tongue': tongue_stim, 'legs': legs_stim}

    def _init_labels(self):
        """
        This method creates dict containing a stimulus vector
        :return: the stimulus in each trial (list)
        """

        # Create the balance label vector
        for i in self.enum_image.keys():
            self.labels += [i] * (self.num_trials // len(self.enum_image.keys()))
        self.labels += list(np.random.choice(list(self.enum_image.keys()),
                                             size=self.num_trials % len(self.enum_image.keys()),
                                             replace=True))
        random.shuffle(self.labels)

        # Save the labels as csv file
        pd.DataFrame.from_dict({'name': self.labels}).to_csv(os.path.join(self.subject_directory, 'labels.csv'),
                                                             index=False, header=False)

    def _user_messages(self, trial_index):
        """
        Show for the user messages in the following order:
            1. Next message
            2. Cue for the trial condition
            3. Ready & state message
        :param trial_index: the index of the current trial
        :return:
        """

        color = self.visual_params['text_color']
        height = self.visual_params['text_height']
        trial_image = self.enum_image[self.labels[trial_index]]
        win = self.window_params['main_window']

        # Show 'next' message
        next_message = visual.TextStim(win, 'The next stimulus is...', color=color, height=height)
        next_message.draw()
        win.flip()
        time.sleep(self.next_length)

        # Show cue
        cue = visual.ImageStim(win, self.images_path[trial_image])
        cue.draw()
        win.flip()
        time.sleep(self.cue_length)

        # Show ready & state message
        state_text = 'Trial: {} / {}'.format(trial_index + 1, self.num_trials)
        state_message = visual.TextStim(win, state_text, pos=[0, -250], color=color, height=height)
        ready_message = visual.TextStim(win, 'Ready...', pos=[0, 0], color=color, height=height)
        ready_message.draw()
        state_message.draw()
        win.flip()
        time.sleep(self.ready_length)

    def _show_stimulus(self, trial_index):
        """
        Show the current condition on screen and wait.
        Additionally response to shutdown key.
        :param trial_index: the current trial index
        :return:
        """

        # Params
        win = self.window_params['main_window']
        trial_img = self.enum_image[self.labels[trial_index]]

        # Get the current stimulus on draw it on screen
        self.window_params[trial_img].draw()
        win.flip()
        time.sleep(self.trial_length)

        # Halt if escape was pressed
        if 'escape' == self.get_keypress():
            sys.exit(-1)

    def _extract_trials(self) -> List[pd.DataFrame]:
        """
        The method extract from the offline experiment collected EEG data and split it into trials.
        The method export a pickle file to the subject directory with a list with all the trials.
        :return: list of trials where each trial is a pandas DataFrame
        """

        # Wait for a sec to the OpenBCI to get the last marker
        time.sleep(0.5)

        # Extract the data
        trials = []
        data = self.eeg.get_board_data()
        ch_names = self.eeg.get_board_names()
        ch_channels = self.eeg.get_board_channels()
        durations, labels = self.eeg.extract_trials(data)

        # Assert the labels
        assert self.labels == labels, 'The labels are not equals to the extracted labels'

        # Append each
        for start, end in durations:
            trial = data[ch_channels, start:end]
            trials.append(pd.DataFrame(data=trial.T, columns=ch_names))

        # Dump to pickle
        pickle.dump(trials, open(os.path.join(self.subject_directory, 'trials.pickle'), 'wb'))

        return trials

    def run(self):

        # Update the directory for the current subject
        self._init_directory()
        messagebox.showinfo(title='bci4als', message='Start running trials...')

        # Init psychopy and screen params
        self._init_window()

        # Init label vector
        self._init_labels()

        # Start stream
        self.eeg.on()

        # Run trials
        for i in range(self.num_trials):
            # Messages for user
            self._user_messages(i)

            # Show the stimulus
            self.eeg.insert_marker(status='start', label=self.labels[i], index=i)
            self._show_stimulus(i)

            # Push end-trial marker
            self.eeg.insert_marker(status='stop', label=self.labels[i], index=i)

        # Export and return the data
        trials = self._extract_trials()
        self.eeg.off()

        return trials, self.labels
