import os
import time
from collections import namedtuple
from typing import Dict
from psychopy import visual

# name tuple object for the progress bar params
Bar = namedtuple('Bar', ['pos', 'line_size', 'frame_size', 'frame_color', 'fill_color'])


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
        self.stop = False
        self.progress: float = 0
        self.refresh_rate: float = refresh_rate
        self.buffer_time: float = buffer_time

        # Images params
        self.images_path: Dict[str, str] = {
            'right': os.path.join(os.path.dirname(__file__), 'images', 'arrow_right.jpeg'),
            'left': os.path.join(os.path.dirname(__file__), 'images', 'arrow_left.jpeg'),
            'idle': os.path.join(os.path.dirname(__file__), 'images', 'square.jpeg'),
            'tongue': os.path.join(os.path.dirname(__file__), 'images', 'tongue.jpeg'),
            'legs': os.path.join(os.path.dirname(__file__), 'images', 'legs.jpeg')}
        self.enum_image = {0: 'right', 1: 'left', 2: 'idle', 3: 'tongue', 4: 'legs'}

        # Progress bars params
        self.bar: Bar = Bar(pos=(0, -0.5), line_size=(0.01, 0.4), frame_size=(1.9, 0.2),
                            frame_color='white', fill_color='green')
        self.time_bar: Bar = Bar(pos=(0, -0.8), line_size=None, frame_size=(1, 0.1),
                                 frame_color='white', fill_color='white')

        # Psychopy objects
        self.win: visual.Window = win
        self.img_stim: visual.ImageStim = visual.ImageStim(self.win, image=self.images_path[self.enum_image[self.stim]])
        self.center_line: visual.Rect = visual.Rect(self.win, pos=self.bar.pos, size=self.bar.line_size,
                                                    lineColor=None, fillColor=self.bar.frame_color, autoDraw=False)
        self.feedback_frame: visual.Rect = visual.Rect(self.win, pos=self.bar.pos, size=self.bar.frame_size,
                                                       lineColor=self.bar.frame_color, fillColor=None, autoDraw=True)
        self.feedback_bar: visual.Rect = visual.Rect(self.win, pos=(0, self.feedback_frame.pos[1]),
                                                     size=(0, self.feedback_frame.size[1]),
                                                     lineColor=self.bar.frame_color, fillColor=self.bar.fill_color)

        # Time bar object
        self.time_bar_frame: visual.Rect = visual.Rect(win=self.win, pos=self.time_bar.pos,
                                                       size=self.time_bar.frame_size,
                                                       lineColor=self.time_bar.frame_color, autoDraw=True)
        self.time_bar: visual.Rect = visual.Rect(win=self.win, pos=(0, self.time_bar_frame.pos[1]),
                                                 size=(0, self.time_bar_frame.size[1]),
                                                 fillColor=self.time_bar.fill_color)

    def update(self, predict_stim: int, skip: bool = False):
        """
        Update the feedback on screen.
        The update occur according to the model prediction. If the model was right
        the progress bar get wider, otherwise it stay the same size.
        :param predict_stim: prediction of the model.
        :param skip: optionally skip this stimulus.
        :return:
        """
        # If the model predicted right
        if predict_stim == self.stim:
            self.progress += 1 / self.threshold

            if self.progress == 1:
                self.confident = True
                self.stop = True

        if skip:
            self.stop = True

    def display(self, current_time: float):
        """
        Display the current state of the progress bar aside to the current stim
        :param current_time: the current time for the time bar object
        :return:
        """

        self._draw_feedback()

        self._draw_time_bar(current_time)

        # If time to stop trial draw finished message
        if self.stop:
            if self.confident:
                text = 'Well done!\nPress any key to continue'
            else:
                text = 'Skipping.\nPress any key to continue'
            visual.TextStim(self.win, text, pos=(0, 0.5)).draw()

        # Display window & wait
        self.win.flip()
        time.sleep(self.refresh_rate)

        # todo: Set auto draw to false

    def _draw_feedback(self):
        """
        Draw feedback on win according to the current state.
        :return:
        """

        # Update feedback size & pos
        self.feedback_bar.width = self.progress * self.bar.frame_size[0]
        self.feedback_bar.pos[0] = self.feedback_frame.pos[
                                       0] - self.feedback_frame.width / 2 + self.feedback_bar.width / 2

        # Draw elements
        self.img_stim.draw()  # always keep the draw of the image first
        self.feedback_bar.draw()

    def _draw_time_bar(self, current_time: float):
        """
        Draw time bar on win according to the current time
        :param current_time: the current time in the experiment from the range [0, buffer_time]
        :return:
        """

        # Update size & pos
        self.time_bar.width = current_time / self.buffer_time
        self.time_bar.pos[0] = self.time_bar_frame.pos[0] - self.time_bar_frame.width / 2 + self.time_bar.width / 2

        # Draw
        self.time_bar.draw()
