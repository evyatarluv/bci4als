import os
from typing import Dict
from collections import namedtuple
from psychopy import visual, event

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

        win (visual.Window)
            The psychopy window of the experiment.

    """
    def __init__(self, stim, threshold=3):

        self.stim: int = stim
        self.threshold: int = threshold
        self.confident: bool = False
        self.progress: float = 0

        # Images params
        self.images_path: Dict[str, str] = {
            'right': os.path.join(os.path.dirname(__file__), 'images', 'arrow_right.jpeg'),
            'left': os.path.join(os.path.dirname(__file__), 'images', 'arrow_left.jpeg'),
            'idle': os.path.join(os.path.dirname(__file__), 'images', 'square.jpeg')}
        self.enum_image = {0: 'right', 1: 'left', 2: 'idle'}

        # Progress bar params
        self.bar: Bar = Bar(pos=(0, -0.5), line_size=(0.01, 0.4), frame_size=(1.9, 0.2),
                            frame_color='white', fill_color='green')

        # Psychopy window
        # Maybe get it as argument
        self.win = visual.Window(monitor='testMonitor', fullscr=False)

        # Start display
        self._display()

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

            self._display()

    def _display(self):
        """
        Display the current state of the progress bar aside to the current stim
        :return:
        """

        # Compute current progress size
        progress_pos, progress_size = self._compute_progress_display()

        # Stim
        img_stim = visual.ImageStim(self.win, image=self.images_path[self.enum_image[self.stim]])

        # Progress bar
        progress_bar = visual.Rect(self.win, pos=progress_pos, size=progress_size,
                                   lineColor=self.bar.frame_color, fillColor=self.bar.fill_color)
        center_line = visual.Rect(self.win, pos=self.bar.pos, size=self.bar.line_size,
                                  lineColor=None, fillColor=self.bar.frame_color)
        bar_frame = visual.Rect(self.win, pos=self.bar.pos, size=self.bar.frame_size,
                                lineColor=self.bar.frame_color, fillColor=None)

        # Display all
        img_stim.draw()
        progress_bar.draw()
        center_line.draw()
        bar_frame.draw()
        self.win.flip()

        # Debug
        event.waitKeys()

    def _compute_progress_display(self):

        # Direction of the progress (1 -> right, -1 -> left)
        direction = 1 if self.stim == 0 else -1

        # Compute the current width
        width = self.progress * self.bar.frame_size[0] / 2

        # Compute the current x location
        x = self.bar.pos[0] + width / 2

        # Pack width and x as size and pos
        size = (width, self.bar.frame_size[1])
        pos = (x, self.bar.pos[1])

        return pos, size


class OnlineExperiment:

    def run_experiment(self):
