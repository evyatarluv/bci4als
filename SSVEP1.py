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

low_end = 7  # lower bound of target frequency
high_end = 24  # higher bound of target frequency
freq_step = 1  # difference between each neighboring frequency

visual_params = {
    'white_rect_size': 180,
    'green_rect_size': 200,
}

stimulus_params = {
    'refresh_rate': 100,  # refresh rate for the monitor
    'condition_freq': [7, 17],  # which frequencies to create
    'stim_time': 5  # overall time of sequence
}


def plot_figure(sin, binary, t, freq):

    plt.plot(t, sin)
    plt.plot(t, binary)
    plt.title('Frequency = {}'.format(freq))
    plt.show()


def binary_stim_init(figure_flag=False):

    """
    This function creates dict containing a binary sequence of sine waves
    :param figure_flag: would you like to show the output waves? (bool)
    :return: dict with all frequencies binary sequence
    """

    # Set params
    refresh_rate = stimulus_params['refresh_rate']
    condition_freq = stimulus_params['condition_freq']
    stim_time = stimulus_params['stim_time']

    dt = 1 / refresh_rate
    t = np.arange(0, stim_time, dt)

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


def window_init():

    green_size = visual_params['green_rect_size']
    rect_size = visual_params['white_rect_size']

    # create the main window
    # will change later to full-screen mode
    main_window = visual.Window([800, 600], monitor="testMonitor", units="pix")

    # Create green rectangle
    green_rect = visual.Rect(win=main_window, size=[green_size, green_size], units='pix', lineColor='green')

    # Create white rectangles according to the num_target
    white_rect = []
    spacing = (main_window.size[0] - (rect_size * num_targets)) / (num_targets + 1)
    current_pos = -main_window.size[0] / 2

    for i in range(1, num_targets + 1):

        current_pos += spacing + (rect_size / 2)
        white_rect.append(visual.Rect(win=main_window, size=[rect_size, rect_size], pos=[current_pos, 0],
                                      units='pix', lineColor=None, fillColor='white'))
        current_pos += rect_size / 2

    return main_window, white_rect, green_rect


def prepare_training():

    # Which rectangle is the rectangle with the green rect surround him,
    # in each trial
    training_vector = rnd.choices(range(num_targets), k=num_trials)
    # TODO: save this vector

    # What is the frequency of the chosen rectangle
    session_freq = [stimulus_params['condition_freq'][i] for i in training_vector]
    # TODO: save this vector

    return training_vector, session_freq


def ready_message(main_window):

    ready_text = visual.TextStim(main_window, 'Ready', pos=[0, 0], color='white')
    ready_text.draw()
    main_window.flip()
    time.sleep(2)


def show_stimulus(main_window, white_rect, green_rect, condition_binary, training_vector):
    pass


def main():

    # TODO: init LSL

    main_window, white_rect, green_rect = window_init()

    condition_binary = binary_stim_init(figure_flag=False)

    training_vector,  = prepare_training()

    # Run trials
    for i in range(num_trials):

        current_trial = training_vector[i]
        # current_freq = ??

        ready_message(main_window)

        show_stimulus(main_window, white_rect, green_rect, condition_binary, training_vector)

    # Debug - show the screen
    # draw the stimuli and update the window
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