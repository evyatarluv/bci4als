# todo: add description of the code

from psychopy import visual, core, event
import numpy as np
import time
import pylsl
import os
import pandas as pd

# Params
recording_folder = 'C:\\Users\\lenovo\\Documents\\CurrentStudy'  # folder to locate the subject folder

lsl_params = {
    'start_experiment': '1111',
    'start_trial': '111',
    'end_experiment': '99',
}

visual_params = {
    'image_path': {'right': 'MI_images/arrow_right.jpeg',
                   'left': 'MI_images/arrow_left.jpeg',
                   'idle': 'MI_images/square.jpeg'},
    'text_height': 48,
    'text_color': 'white'
}

experiment_params = {
    'enumerate_stim': {0: 'right', 1: 'left', 2: 'idle'},  # dict which translate from stim to num
    'num_trials': 30,  # set number of training trials
    'trial_length': 5,  # seconds of each trial
    'cue_length': 0.25,  # seconds of cure before the 'Ready' message
    'ready_length': 1,  # seconds of 'Ready' message before starting the next trial
    'next_length': 1,  # seconds of 'Next' message before the cue
}


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
    main_window = visual.Window([1280, 720], monitor='testMonitor', units='pix', color='black', fullscr=False)

    # Create right, left and idle stimulus
    right_stim = visual.ImageStim(main_window, image=visual_params['image_path']['right'])
    left_stim = visual.ImageStim(main_window, image=visual_params['image_path']['left'])
    idle_stim = visual.ImageStim(main_window, image=visual_params['image_path']['idle'])

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

    color = visual_params['text_color']
    height = visual_params['text_height']
    trial_image = visual_params['image_path'][experiment_params['enumerate_stim'][current_trial]]

    # Show 'next' message
    next_message = visual.TextStim(main_window, 'The next stimulus is...', color=color, height=height)
    next_message.draw()
    main_window.flip()
    time.sleep(experiment_params['next_length'])

    # Show cue
    cue = visual.ImageStim(main_window, trial_image)
    cue.draw()
    main_window.flip()
    time.sleep(experiment_params['cue_length'])

    # Show ready & state message
    state_text = 'Trial: #{} from {}'.format(trial_index + 1, experiment_params['num_trials'])
    state_message = visual.TextStim(main_window, state_text, pos=[0, -250], color=color, height=height)
    ready_message = visual.TextStim(main_window, 'Ready...', pos=[0, 0], color=color, height=height)
    ready_message.draw()
    state_message.draw()
    main_window.flip()
    time.sleep(experiment_params['ready_length'])


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

    print(message)
    win.close()
    core.quit()


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
    psychopy_params[experiment_params['enumerate_stim'][current_trial]].draw()
    main_window.flip()
    time.sleep(experiment_params['trial_length'])

    # Halt if escape was pressed
    if 'escape' == get_keypress():
        shutdown_training(main_window, 'User pressed `escape`, shutdown immediately')


def init_lsl():

    """
    Define the stream parameters and create outlet stream.
    :return: outlet stream object
    """

    info = pylsl.StreamInfo('MarkerStream', 'Markers', 1, 0, 'string', 'myuniquesourceid23443')
    outlet_stream = pylsl.StreamOutlet(info)

    print('\nOpen Lab Recorder & check for MarkerStream and EEG stream')
    input('Start recording and hit any enter to continue')

    return outlet_stream


def init_directory():

    """
    init the current subject directory
    :return: the subject directory
    """

    while True:

        # Get the subject id
        subject_id = input('Please enter subject ID: ')

        # Update the recording folder directory
        subject_folder = recording_folder + '\\' + subject_id

        try:
            # Create new folder for the current subject
            os.mkdir(subject_folder)
            print('The subject folder was created successfully')
            return subject_folder

        except Exception as e:
            print('An {} exception occurred, insert subject ID again'.format(type(e).__name__))


def MI_training():

    # Update the directory for the current subject
    subject_folder = init_directory()

    # Init the LSL
    outlet_stream = init_lsl()

    # Init psychopy and screen params
    psychopy_params = window_init()

    # Built the stimulus vector
    stim_vector = init_stim_vector(experiment_params['num_trials'], subject_folder)

    # Push marker to mark the start of the experiment
    outlet_stream.push_sample([lsl_params['start_experiment']])

    # Run trials
    print('\nStart running trials...')
    for i in range(experiment_params['num_trials']):

        # Get the current trial
        current_trial = stim_vector[i]

        # Messages for user
        user_messages(psychopy_params['main_window'], current_trial, i)

        # Push LSL samples for trial's start and condition
        outlet_stream.push_sample([lsl_params['start_trial']])
        outlet_stream.push_sample([str(current_trial)])

        # Show the stimulus
        show_stimulus(current_trial, psychopy_params)

    # End experiment
    outlet_stream.push_sample([lsl_params['end_experiment']])
    shutdown_training(psychopy_params['main_window'], 'Stop the LabRecording recording')


if __name__ == '__main__':

    MI_training()

