import os
import sys
import time
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askdirectory
from typing import Dict, List, Any
import numpy as np
import pandas as pd
from psychopy import visual, event
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds


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


class OfflineExperiment:

    def __init__(self, num_trials, trial_length, next_length=1, cue_length=0.25, ready_length=1):

        self.subject_directory: str = ''
        self.num_trials: int = num_trials
        self.window_params: Dict[str, Any] = {}
        self.labels: List[int] = []
        self.cue_length: float = cue_length
        self.next_length: float = next_length
        self.ready_length: float = ready_length
        self.trial_length: float = trial_length

        self.images_path: Dict[str, str] = {
            'right': os.path.join(os.path.dirname(__file__), 'images', 'arrow_right.jpeg'),
            'left': os.path.join(os.path.dirname(__file__), 'images', 'arrow_left.jpeg'),
            'idle': os.path.join(os.path.dirname(__file__), 'images', 'square.jpeg')}
        self.enum_image = {0: 'right', 1: 'left', 2: 'idle'}
        self.visual_params: Dict[str, Any] = {'text_color': 'white', 'text_height': 48}
        self.board: BoardShim = None

    def _init_directory(self):
        """
        init the current subject directory
        :return: the subject directory
        """

        # get the CurrentStudy recording directory
        if not messagebox.askokcancel(title='bci4als',
                                      message="Welcome to the motor imagery EEG recorder."
                                              "\n\nNumber of trials: {}\n\n"
                                              "Please select the CurrentStudy directory:".format(self.num_trials)):
            sys.exit(-1)

        recording_folder = askdirectory()  # show an "Open" dialog box and return the path to the selected file
        if not recording_folder:
            sys.exit(-1)

        while True:
            # Get the session id
            session_id = simpledialog.askstring('bci4als', "Please enter a new Session ID:")

            # Update the recording folder directory
            session_folder = os.path.join(recording_folder, session_id)

            try:
                # Create new folder for the current subject
                os.mkdir(session_folder)
                messagebox.showinfo(title='bci4als',
                                    message='The session folder was created successfully.')
                self.subject_directory = session_folder
                return

            except Exception as e:
                if not messagebox.askretrycancel(title='bci4als',
                                                 message='Exception Raised: {}. Please insert a new subject ID:'.format(
                                                     type(e).__name__)):
                    sys.exit(-1)

    def _init_window(self):
        """
        init the psychopy window
        :return: dictionary with the window, left arrow, right arrow and idle.
        """

        # Create the main window
        main_window = visual.Window([1280, 720], monitor='testMonitor', units='pix', color='black', fullscr=False)

        # Create right, left and idle stimulus
        right_stim = visual.ImageStim(main_window, image=self.images_path['right'])
        left_stim = visual.ImageStim(main_window, image=self.images_path['left'])
        idle_stim = visual.ImageStim(main_window, image=self.images_path['idle'])

        self.window_params = {'main_window': main_window, 'right': right_stim, 'left': left_stim, 'idle': idle_stim}

    def _init_labels(self):
        """
        This method creates dict containing a stimulus vector
        :return: the stimulus in each trial (list)
        """

        # Create the labels
        labels = (np.random.choice([0, 1, 2], self.num_trials, replace=True))

        # Save the labels as csv file
        pd.DataFrame.from_dict(labels).to_csv(os.path.join(self.subject_directory, 'labels.csv'),
                                              index=False, header=False)

        self.labels = list(labels)

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
        if 'escape' == get_keypress():
            sys.exit(-1)

    def run(self, ip_port, serial_port):

        # Update the directory for the current subject
        self._init_directory()
        messagebox.showinfo(title='bci4als', message='Start running trials...')

        # Init Board
        self._init_board(ip_port, serial_port)

        # Init psychopy and screen params
        self._init_window()

        # Init label vector
        self._init_labels()

        # Start stream
        self.board.start_stream(int(125 * self.trial_length * self.num_trials * 1.15))

        # Run trials
        for i in range(self.num_trials):

            # Messages for user
            self._user_messages(i)

            # Show the stimulus
            # todo: Stopped here
            # self.board.insert_marker(self._encode_marker())
            self._show_stimulus(i)

    def _init_board(self, ip_port, serial_port):

        params = BrainFlowInputParams()
        params.ip_port = ip_port
        params.serial_port = serial_port
        self.board = BoardShim(BoardIds.CYTON_DAISY_BOARD.value, params)
        self.board.prepare_session()

    def _encode_marker(self, status, label, index):
        raise NotImplementedError
        # todo: Stopped here
