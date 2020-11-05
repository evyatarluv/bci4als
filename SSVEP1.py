from psychopy import visual, core, event  # import some libraries from PsychoPy
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import time
import pylsl
import os
import pandas as pd

# Params
trial_length = 5  # each trial length in seconds

num_trials = 30  # set number of training trials

num_targets = 2  # set number of possible targets

condition_freq = [7, 17]  # frequency vectors for each target (length must correspond to num_targets)

recording_folder = 'C:\\Users\\lenovo\\Documents\\CurrentStudy'  # folder to locate the subject folder

lsl_params = {
    'start_experiment': '1111',
    'start_trial': '111',
    'end_experiment': '99',
}

visual_params = {
    'white_rect_size': 180,
    'green_rect_size': 200,
}


def plot_figure(sin, binary, t, freq):

    plt.plot(t, sin)
    plt.plot(t, binary)
    plt.title('Frequency = {}'.format(freq))
    plt.show()


def binary_stim_init(refresh_rate, subject_folder, figure_flag=False):

    """
    This function creates dict containing a binary sequence of sine waves
    :param subject_folder: the directory of the current subject
    :param refresh_rate: refresh rate for the monitor
    :param figure_flag: would you like to show the output waves? (bool)
    :return: dict with all frequencies binary sequence
    """

    dt = 1 / refresh_rate
    t = np.arange(0, trial_length, dt)

    sine_waves = {}  # save the sine wave in order to plot it
    binary_vector = {}  # the final binary vector for each freq

    # For each frequency in the dynamic_range
    for freq in condition_freq:

        sine_waves[freq] = np.sin(2 * np.pi * freq * t)  # create sin wave
        binary_vector[freq] = np.where(sine_waves[freq] > 0, 1, 0)  # transform to binary vector

        # Debug visualization
        if figure_flag:
            plot_figure(sine_waves[freq], binary_vector[freq], t, freq)

    # Save the binary vector as csv file
    pd.DataFrame.from_dict(binary_vector).to_csv(subject_folder + '\\binary_vectors.csv', index=False)

    return binary_vector


def create_white_rect(main_window, rect_size):

    # Params
    white_rect = []
    spacing = (main_window.size[0] - (rect_size * num_targets)) / (num_targets + 1)  # space between two rect
    current_pos = -main_window.size[0] / 2  # current position for locating the next rect

    # Creating & locating the rectangles
    for i in range(1, num_targets + 1):
        current_pos += spacing + (rect_size / 2)
        white_rect.append(visual.Rect(win=main_window, size=[rect_size, rect_size], pos=[current_pos, 0],
                                      units='pix', lineColor=None, fillColor='white'))
        current_pos += rect_size / 2

    return white_rect


def window_init():

    """
    init the psychopy window
    :return: dictionary with the window, white rect and green rect
    """

    green_size = visual_params['green_rect_size']
    rect_size = visual_params['white_rect_size']

    # create the main window
    main_window = visual.Window([1280, 720], monitor="testMonitor", units="pix", fullscr=True)

    # Create green rectangle
    green_rect = visual.Rect(win=main_window, size=[green_size, green_size], units='pix', lineColor='green')

    # Create white rectangles and locate them on screen
    white_rect = create_white_rect(main_window, rect_size)

    return {'main_window': main_window, 'white_rect': white_rect, 'green_rect': green_rect}


def prepare_training(subject_folder):

    """
    The function create two list for the training part.
    The first list include the index of the white rect which surrounded with green frame in the specific trial.
    For example: surrounded_index[i] = j means that in the i trial the j rectangle is surrounded.
    The second list include the frequency of the surrounded rectangle.
    For example: surrounded_freq[i] = j means that in the i trial the surrounded rectangle showed in frequency j.
    :return: two lists
    """

    # Which rectangle is the rectangle with the green rect surround him in each trial
    surrounded_index = rnd.choices(range(num_targets), k=num_trials)

    # What is the frequency of the chosen rectangle
    surrounded_freq = [condition_freq[i] for i in surrounded_index]

    # Save both vectors
    pd.DataFrame.from_dict({
        'trial': range(1, num_trials + 1),
        'surrounded_index': surrounded_index,
        'surrounded_freq': surrounded_freq
    }).to_csv(subject_folder + '\\training_trials.csv', index=False)

    return surrounded_index, surrounded_freq


def ready_message(main_window):

    ready_text = visual.TextStim(main_window, 'Ready', pos=[0, 0], color='white')
    ready_text.draw()
    main_window.flip()
    time.sleep(2)


def get_keypress():
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


def show_stimulus(condition_binary, surrounded_rect_index, screen_params, psychopy_params):

    # Exclude params from dictionaries
    num_frames = screen_params['num_frames']
    main_window = psychopy_params['main_window']
    white_rect = psychopy_params['white_rect']
    green_rect = psychopy_params['green_rect']

    # Show the green rectangle first
    green_rect.pos = white_rect[surrounded_rect_index].pos
    green_rect.draw()
    main_window.flip()
    time.sleep(2)

    # For each frame decide for each rect if to show it or hide it by his frequency
    # Debug - measure time of trials
    start_trial = time.time()
    for frame in range(num_frames):

        # Clear the screen
        main_window.clearBuffer()

        # For each frequency & rectangle index
        for rect_index, freq in enumerate(condition_binary):

            if condition_binary[freq][frame] == 1:

                white_rect[rect_index].draw()

        # Show the green rectangle
        green_rect.pos = white_rect[surrounded_rect_index].pos
        green_rect.draw()

        # Flip the screen
        main_window.flip()

        # Halt if escape was pressed
        if 'escape' == get_keypress():
            shutdown_training(main_window, 'User pressed `escape`, shutdown immediately')

    # Debug - measure time of trial
    print('Trial duration: {} (s)'.format(round(time.time() - start_trial, 3)))


def get_screen_params(window):

    refresh_rate = 1 / window.monitorFramePeriod

    num_frames = int(np.floor(trial_length / window.monitorFramePeriod))

    wait_frames = 1

    return {'refresh_rate': refresh_rate, 'num_frames': num_frames, 'wait_frames': wait_frames}


def trial_state_message(main_window, current_trial, total_trials):

    trial_state = 'Trial: #{} from {}'.format(current_trial + 1, total_trials)

    ready_text = visual.TextStim(main_window, trial_state, pos=[0, 0], color='white')
    ready_text.draw()
    main_window.flip()
    time.sleep(2)


def init_lsl():

    """
    Define the stream parameters and create outlet stream.
    :return: outlet stream object
    """

    info = pylsl.StreamInfo('MarkerStream', 'Markers', 1, 0, 'string', 'myuniquesourceid23443')
    outlet_stream = pylsl.StreamOutlet(info)

    print('\nOpen Lab Recorder & check for MarkerStream and EEG stream')
    input('Start recording and hit any key to continue')

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


def main():

    # Update the directory for the current subject
    subject_folder = init_directory()

    # Init the LSL
    outlet_stream = init_lsl()

    # Init psychopy and screen params
    psychopy_params = window_init()
    screen_params = get_screen_params(psychopy_params['main_window'])

    # Building the binary stimulus vectors
    condition_binary = binary_stim_init(refresh_rate=screen_params['refresh_rate'],
                                        subject_folder=subject_folder,
                                        figure_flag=False)

    # Prepare set of training trials
    surrounded_index, surrounded_freq = prepare_training(subject_folder)

    # Push marker to mark the start of the experiment
    outlet_stream.push_sample([lsl_params['start_experiment']])

    # Run trials
    print('\nStart running trials')
    for i in range(num_trials):

        # Update the current surrounded rectangle index & frequency
        surrounded_rect_index = surrounded_index[i]
        surrounded_rect_freq = surrounded_freq[i]

        # Messages for user
        ready_message(psychopy_params['main_window'])
        trial_state_message(psychopy_params['main_window'], i, num_trials)

        # Push LSL samples for start trial and the trial's conditions
        outlet_stream.push_sample([lsl_params['start_trial']])
        outlet_stream.push_sample([str(surrounded_rect_index)])
        outlet_stream.push_sample([str(surrounded_rect_freq)])

        # Show the stimulus
        show_stimulus(condition_binary, surrounded_rect_index, screen_params, psychopy_params)

    # End experiment
    outlet_stream.push_sample([lsl_params['end_experiment']])
    shutdown_training(psychopy_params['main_window'], 'Stop the LabRecording recording')


if __name__ == '__main__':

    main()