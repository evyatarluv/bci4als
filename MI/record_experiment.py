"""

Motor Imagery Training
This script creates a training paradigm with 3 targets on screen for
given num of trials. Before each trial, one of the targets is cued (and remains
cued for the entire trial).This code assumes EEG is recorded and streamed
through LSL for later offline preprocessing and model learning.

"""

import os
import time
import sys
from tkinter import Tk, messagebox, simpledialog
from tkinter.filedialog import askdirectory

import numpy as np
import pandas as pd
import pylsl
from psychopy import visual, event
from MI.config import params

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing


def init_stim_vector(trials_num, subject_folder):
    """
    This function creates dict containing a stimulus vector
    :param trials_num: number of trials in the experiment
    :param subject_folder: the directory of the current subject
    :return: the stimulus in each trial (list)
    """

    # Create the stimulus vector
    stim_vector = np.random.choice([0, 1, 2], trials_num, replace=True)

    # Save the binary vector as csv file
    pd.DataFrame.from_dict(stim_vector).to_csv(subject_folder + '\\stimulus_vectors.csv',
                                               index=False, header=False)

    return stim_vector


def window_init():
    """
    init the psychopy window
    :return: dictionary with the window, left arrow, right arrow and idle.
    """

    # Create the main window
    main_window = visual.Window([1280, 720], monitor='testMonitor', units='pix', color='black', fullscr=True)

    # Create right, left and idle stimulus
    right_stim = visual.ImageStim(main_window, image=params['visual']['images']['right'])
    left_stim = visual.ImageStim(main_window, image=params['visual']['images']['left'])
    idle_stim = visual.ImageStim(main_window, image=params['visual']['images']['idle'])

    return {'main_window': main_window, 'right': right_stim, 'left': left_stim, 'idle': idle_stim}


def user_messages(main_window, current_trial, trial_index):
    """
    Show for the user messages in the following order:
        1. Next message
        2. Cue for the trial condition
        3. Ready & state message
    :param trial_index: the index of the current trial (int)
    :param current_trial: the condition of the current trial (int)
    :param main_window: psychopy window
    :return:
    """

    color = params['visual']['text_color']
    height = params['visual']['text_height']
    trial_image = params['visual']['image_path'][params['experiment']['enumerate_stim'][current_trial]]

    # Show 'next' message
    next_message = visual.TextStim(main_window, 'The next stimulus is...', color=color, height=height)
    next_message.draw()
    main_window.flip()
    time.sleep(params['experiment']['next_length'])

    # Show cue
    cue = visual.ImageStim(main_window, trial_image)
    cue.draw()
    main_window.flip()
    time.sleep(params['experiment']['cue_length'])

    # Show ready & state message
    state_text = 'Trial: {} / {}'.format(trial_index + 1, params['experiment']['num_trials'])
    state_message = visual.TextStim(main_window, state_text, pos=[0, -250], color=color, height=height)
    ready_message = visual.TextStim(main_window, 'Ready...', pos=[0, 0], color=color, height=height)
    ready_message.draw()
    state_message.draw()
    main_window.flip()
    time.sleep(params['experiment']['ready_length'])


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


def shutdown_training(win, message):
    """
    Shutdown the psychopy window after printing a message
    :param win: psychopy window
    :param message: shutdown message
    :return:
    """

    win.close()
    messagebox.showinfo(title=params['gui']['title'],
                        message='Stop Lab Recorder!\nClick okay to exit experiment.')


def show_stimulus(current_trial, psychopy_params):
    """
    Show the current condition on screen and wait.
    Additionally response to shutdown key.
    :param current_trial: the current condition (int)
    :param psychopy_params: main window and all the stimulus
    :return:
    """

    # Params
    main_window = psychopy_params['main_window']

    # Get the current stimulus on draw it on screen
    psychopy_params[params['experiment']['enumerate_stim'][current_trial]].draw()
    main_window.flip()
    time.sleep(params['experiment']['trial_length'])

    # Halt if escape was pressed
    if 'escape' == get_keypress():
        sys.exit(-1)


def init_lsl():
    """
    Define the stream parameters and create outlet stream.
    :return: outlet stream object
    """

    info = pylsl.StreamInfo('MarkerStream', 'Markers', 1, 0, 'string', 'myuniquesourceid23443')
    outlet_stream = pylsl.StreamOutlet(info)

    messagebox.showinfo(title=params['gui']['title'],
                        message='Start Lab Recorder!\nBe sure to check your settings.\nClick okay to begin experiment.')

    return outlet_stream


def init_directory():
    """
    init the current subject directory
    :return: the subject directory
    """

    # get the recording directory
    if not messagebox.askokcancel(title=params['gui']['title'],
                                  message="Welcome to the motor imagery EEG recorder.\n\nNumber of trials: {}\n\nPlease select the CurrentStudy directory:".format(
                                      params['experiment']['num_trials'])):
        sys.exit(-1)

    print("hello")

    # fixme: my running get stuck here
    recording_folder = askdirectory()  # show an "Open" dialog box and return the path to the selected file
    if not recording_folder:
        sys.exit(-1)

    while True:
        # Get the subject id
        subject_id = simpledialog.askstring(params['gui']['title'], "Please enter a new Subject ID:")

        # Update the recording folder directory
        subject_folder = os.path.join(recording_folder, subject_id)

        try:
            # Create new folder for the current subject
            os.mkdir(subject_folder)
            messagebox.showinfo(title=params['gui']['title'],
                                message='The subject folder was created successfully.')
            return subject_folder

        except Exception as e:
            if not messagebox.askretrycancel(title=params['gui']['title'],
                                             message='Exception Raised: {}. Please insert a new subject ID:'.format(
                                                 type(e).__name__)):
                sys.exit(-1)


def MI_record():
    # Update the directory for the current subject
    subject_folder = init_directory()

    # Init the LSL
    outlet_stream = init_lsl()

    # Run trials
    messagebox.showinfo(title=params['gui']['title'],
                        message='Start running trials...')

    # Init psychopy and screen params
    psychopy_params = window_init()

    # Build the stimulus vector
    stim_vector = init_stim_vector(params['experiment']['num_trials'], subject_folder)

    # Push marker to mark the start of the experiment
    outlet_stream.push_sample([params['lsl']['start_experiment']])

    for i in range(params['experiment']['num_trials']):
        # Get the current trial
        current_trial = stim_vector[i]

        # Messages for user
        user_messages(psychopy_params['main_window'], current_trial, i)

        # Push LSL samples for trial's start
        outlet_stream.push_sample([params['lsl']['start_trial']])

        # Show the stimulus
        show_stimulus(current_trial, psychopy_params)

        # Push LSL end trial
        outlet_stream.push_sample([params['lsl']['end_trial']])

    # End experiment
    outlet_stream.push_sample([params['lsl']['end_experiment']])
    shutdown_training(psychopy_params['main_window'], 'Stop the LabRecording recording')


def record_experiment(paradigm='MI'):
    if paradigm.lower() in ['mi', 'motor imagery']:
        MI_record()

    elif paradigm.lower() in ['SSVEP']:
        raise NotImplementedError()

    else:
        raise ValueError("Unrecognized paradigm.")


if __name__ == '__main__':
    record_experiment('Motor Imagery')
