from psychopy import visual, core, event  # import some libraries from PsychoPy
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import time

# Params
# TODO: Rearrange the params into dicts
trial_length = 5  # each trial length in seconds
num_trials = 30  # set number of training trials
num_targets = 2  # set number of possible targets
condition_freq = [7, 17]  # frequency vectors for each target (length must correspond to num_targets)

visual_params = {
    'white_rect_size': 180,
    'green_rect_size': 200,
}


def plot_figure(sin, binary, t, freq):

    plt.plot(t, sin)
    plt.plot(t, binary)
    plt.title('Frequency = {}'.format(freq))
    plt.show()


def binary_stim_init(refresh_rate, figure_flag=False):

    """
    This function creates dict containing a binary sequence of sine waves
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

    # TODO: save the binary vector

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
    # will change later to full-screen mode
    main_window = visual.Window([800, 600], monitor="testMonitor", units="pix")

    # Create green rectangle
    green_rect = visual.Rect(win=main_window, size=[green_size, green_size], units='pix', lineColor='green')

    # Create white rectangles and locate them on screen
    white_rect = create_white_rect(main_window, rect_size)

    return {'main_window': main_window, 'white_rect': white_rect, 'green_rect': green_rect}


def prepare_training():
    """
    The function create two list for the training part.
    The first list include the index of the white rect which surrounded with green frame in the specific trial.
    For example: surrounded_index[i] = j means that in the i trial the j rectangle is surrounded.
    The second list include the frequency of the surrounded rectangle.
    For example: surrounded_freq[i] = j means that in the i trial the surrounded rectangle showed in frequency j.
    :return: two lists
    """

    # Which rectangle is the rectangle with the green rect surround him,
    # in each trial
    surrounded_index = rnd.choices(range(num_targets), k=num_trials)
    # TODO: save this vector

    # What is the frequency of the chosen rectangle
    surrounded_freq = [condition_freq[i] for i in surrounded_index]
    # TODO: save this vector

    return surrounded_index, surrounded_freq


def ready_message(main_window):

    ready_text = visual.TextStim(main_window, 'Ready', pos=[0, 0], color='white')
    ready_text.draw()
    main_window.flip()
    time.sleep(2)


def show_stimulus(current_trial, current_freq, condition_binary, training_vector, screen_params, psychopy_params):

    """

    :param current_trial:
    :param current_freq:
    :param condition_binary:
    :param training_vector:
    :param screen_params:
    :param psychopy_params:
    :return:
    """

    # Exclude params from dictionaries
    num_frames = screen_params['num_frames']
    main_window = psychopy_params['main_window']
    white_rect = psychopy_params['white_rect']
    green_rect = psychopy_params['green_rect']

    for frame in range(num_frames):

        pass


def get_screen_params(window):

    refresh_rate = 1 / window.monitorFramePeriod

    num_frames = np.floor(trial_length / window.monitorFramePeriod)

    wait_frames = 1

    return {'refresh_rate': refresh_rate, 'num_frames': num_frames, 'wait_frames': wait_frames}


def trial_state_message(main_window):

    pass


def main():

    # Initialize the LSL
    # TODO: init LSL

    # Initialize psychopy and screen params
    psychopy_params = window_init()
    screen_params = get_screen_params(psychopy_params['main_window'])

    # Building the binary stimulus vectors
    condition_binary = binary_stim_init(refresh_rate=screen_params['refresh_rate'],
                                        figure_flag=False)

    # Prepare set of training trials
    surrounded_index, surrounded_freq = prepare_training()

    # Run trials
    for i in range(num_trials):

        # Update the current surrounded rectangle index & frequency
        current_rect_index = surrounded_index[i]
        current_rect_freq = surrounded_freq[i]

        # Show 'Ready' message on screen
        ready_message(psychopy_params['main_window'])

        # Show trial state message
        # TODO: add this message on screen (?)
        trial_state_message(psychopy_params['main_window'])

        # Push LSL samples for start trial and the trial's conditions
        # TODO: add LSL push: (1111), (current_rect_index), (current_rect_freq)

        # Show the stimulus
        show_stimulus(current_rect_index, current_rect_freq, condition_binary, surrounded_index,
                      screen_params, psychopy_params)

    # Debug - show the screen
    # draw the stimuli and update the window
    white_rect = psychopy_params['white_rect']
    green_rect = psychopy_params['green_rect']
    main_window = psychopy_params['main_window']
    while True:

        green_rect.pos = white_rect[0].pos
        green_rect.draw()

        for r in white_rect:
            r.draw()

        main_window.flip()

        if len(event.getKeys()) > 0:
            break
        event.clearEvents()

    # cleanup
    main_window.close()
    core.quit()


if __name__ == '__main__':

    main()