import os
import time
from typing import Dict
from collections import namedtuple
import random
from bci4als.learning.experiment import Experiment
from psychopy import visual, event, core
from brainflow import BoardShim
import numpy as np
import threading
import multiprocessing

# name tuple object for the progress bar params
Bar = namedtuple('Bar', ['pos', 'line_size', 'frame_size', 'frame_color', 'fill_color'])


def foo():
    print('g')

class Feedback:
    """
    Class for presenting the feedback on the screen.

    Attributes:

        stim (int):
            The current stim the user see and need to imagine.

        threshold (int):
            How many time the model need to predict the stim in order to fill the progress bar.

        confident (bool):
            Is the model predict the correct stim the needed amount of times.

        progress (float):
            The current amount of times the model predict the correct stim.

        images_path (Dict[str, str])
            Dict with stim name as key and path as value.

        enum_image (Dict[int, str])
            Dict for explaining what is number of each image.

        bar (Bar):
            Contain the visual params of the progress bar.

        refresh_rate (float):
            The refresh rate of the feedback in seconds.

        win (visual.Window)
            The psychopy window of the experiment.

    """

    def __init__(self, win: visual.Window, stim: int, buffer_time: float, threshold: int = 3,
                 refresh_rate: float = 0.1):

        self.stim: int = stim
        self.threshold: int = threshold
        self.confident: bool = False
        self.progress: float = 0
        self.refresh_rate: float = refresh_rate
        self.buffer_time: float = buffer_time

        # Images params
        self.images_path: Dict[str, str] = {
            'right': os.path.join(os.path.dirname(__file__), 'images', 'arrow_right.jpeg'),
            'left': os.path.join(os.path.dirname(__file__), 'images', 'arrow_left.jpeg'),
            'idle': os.path.join(os.path.dirname(__file__), 'images', 'square.jpeg')}
        self.enum_image = {0: 'right', 1: 'left', 2: 'idle'}

        # Progress bars params
        self.bar: Bar = Bar(pos=(0, -0.5), line_size=(0.01, 0.4), frame_size=(1.9, 0.2),
                            frame_color='white', fill_color='green')
        self.time_bar: Bar = Bar(pos=(0, -0.8), line_size=None, frame_size=(1, 0.2),
                                 frame_color='white', fill_color='white')

        # Psychopy objects
        self.win: visual.Window = win
        self.center_line: visual.Rect = visual.Rect(self.win, pos=self.bar.pos, size=self.bar.line_size,
                                                    lineColor=None, fillColor=self.bar.frame_color, autoDraw=True)
        self.feedback_frame: visual.Rect = visual.Rect(self.win, pos=self.bar.pos, size=self.bar.frame_size,
                                                       lineColor=self.bar.frame_color, fillColor=None, autoDraw=True)
        self.img_stim: visual.ImageStim = visual.ImageStim(self.win, image=self.images_path[self.enum_image[self.stim]])
        self.feedback_bar: visual.Rect = visual.Rect(self.win, pos=(0, self.feedback_frame.pos[1]),
                                                     size=(0, self.feedback_frame.size[1]),
                                                     lineColor=self.bar.frame_color, fillColor=self.bar.fill_color,
                                                     autoDraw=True)

        # Time bar object
        self.time_bar_frame: visual.Rect = visual.Rect(win=self.win, pos=self.time_bar.pos,
                                                       size=self.time_bar.frame_size,
                                                       lineColor=self.time_bar.frame_color, autoDraw=True)
        self.time_bar: visual.Rect = visual.Rect(win=self.win, pos=(0, self.time_bar_frame.pos[1]),
                                                 size=(0, self.time_bar_frame.size[1]),
                                                 fillColor=self.time_bar.fill_color, autoDraw=True)

        # self.display()
        # Display the feedback with new thread
        # th = threading.Thread(target=self.display)
        # th.start()

    def update(self, predict_stim: int):
        """
        Update the feedback on screen.
        The update occur according to the model prediction. If the model was right
        the progress bar get wider, otherwise it stay the same size.
        :param predict_stim: prediction of the model.
        :return:
        """
        # If the model predicted right
        if predict_stim == self.stim:

            self.progress += 1 / self.threshold

            if self.progress == 1:
                self.confident = True

        self.display()

    def display(self):
        """
        Display the current state of the progress bar aside to the current stim
        :return:
        """

        # Time bar object
        # time_bar_frame = visual.Rect(win=self.win, pos=self.time_bar.pos, size=self.time_bar.frame_size,
        #                              lineColor=self.time_bar.frame_color, autoDraw=True)
        # time_bar = visual.Rect(win=self.win, pos=(0, time_bar_frame.pos[1]), size=(0, time_bar_frame.size[1]),
        #                        fillColor=self.time_bar.fill_color, autoDraw=True)

        timer = core.Clock()

        while True:
            if timer.getTime() > self.buffer_time:
                timer.reset()

            self._draw_feedback()

            self._draw_time_bar(timer.getTime())

            # If confident is True display message
            if self.confident:
                visual.TextStim(self.win, 'Well done!\nPress any key to continue', pos=(0, 0.5)).draw()
                break

            # Display window & wait
            self.win.flip()
            time.sleep(self.refresh_rate)

        # todo: Set auto draw to false

    def _draw_feedback(self):
        """
        Draw feedback on win according to the current state.
        :return:
        """

        direction = 1 if self.stim == 0 else -1

        # Update feedback size & pos
        self.feedback_bar.width = self.progress * self.bar.frame_size[0] / 2
        self.feedback_bar.pos[0] = direction * (self.bar.pos[0] + self.feedback_bar.width / 2)

        # Draw elements
        self.img_stim.draw()

    def _draw_time_bar(self, current_time):
        """
        Draw time bar on win according to the current time
        :param current_time:
        :return:
        """

        # Update size & pos
        self.time_bar.width = current_time / self.buffer_time
        self.time_bar.pos[0] = self.time_bar_frame.pos[0] - self.time_bar_frame.width / 2 + self.time_bar.width / 2


class OnlineExperiment(Experiment):

    def __init__(self, num_trials, buffer_time, threshold, rest_time=2):

        super().__init__(num_trials)
        self.threshold = threshold
        self.buffer_time = buffer_time
        self.rest_time = rest_time

        # self.model = model

    def _init_trials(self):
        """
        Create list with trials as num_trials attributes.
        The trials consist only from right and left (0, 1). Additionally, half of the
        trials be right and half left.
        :return:
        """

        # Calc the amount of right and left
        right_amount = self.num_trials // 2
        left_amount = self.num_trials - right_amount

        # Create the trials list according to the above amounts
        trials = [0] * right_amount + [1] * left_amount

        # Shuffle it
        random.shuffle(trials)

        return trials

    def _get_data(self, board: BoardShim, start_time: float) -> np.ndarray:
        """
        The method return data from the board according to the buffer_time param.

        :param board: board object we get the data from
        :param start_time: the start time of the recording
        :return:
        """
        wait_time = max(0, self.buffer_time - (time.time() - start_time))

        time.sleep(wait_time)

        # return board.get_board_data()
        return None

    def run(self, ip_port, serial_port):

        # Init list of trials
        trials = self._init_trials()

        # Init psychopy window
        win = visual.Window(monitor='testMonitor', fullscr=False)

        # Init board for streaming
        # board = self._init_board(ip_port, serial_port)
        # board.start_stream()  # init exact num_samples?
        board = None

        # For each stim in the trials list
        for stim in trials:

            feedback = Feedback(win, stim, self.buffer_time, self.threshold)

            start_time = time.time()

            while not feedback.confident:

                data = self._get_data(board, start_time)

                start_time = time.time()

                # predict = self.model_predict(data)

                feedback.update(stim)

                # self.model_update(data)

            # Start the next trial
            event.waitKeys()
            board.get_board_data()
