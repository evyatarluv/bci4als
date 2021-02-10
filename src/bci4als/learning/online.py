import os
from typing import Dict

from psychopy import visual, event


class Feedback:

    def __init__(self, stim, threshold=3):

        self.stim: int = stim
        self.threshold: int = threshold
        self.confident: bool = False
        self.progress = 0

        # Images params
        self.images_path: Dict[str, str] = {
            'right': os.path.join(os.path.dirname(__file__), 'images', 'arrow_right.jpeg'),
            'left': os.path.join(os.path.dirname(__file__), 'images', 'arrow_left.jpeg'),
            'idle': os.path.join(os.path.dirname(__file__), 'images', 'square.jpeg')}
        self.enum_image = {0: 'right', 1: 'left', 2: 'idle'}

    def _display(self):

        # Params
        bar_y = -0.5

        # Main window
        win = visual.Window(monitor='testMonitor', fullscr=True)

        # Stim
        img_stim = visual.ImageStim(win, image=self.images_path[self.enum_image[self.stim]])

        # Progress bar
        progress_bar = visual.Rect(win, width=0, height=0.2, pos=(0, bar_y), lineColor='white', fillColor='green')
        center_line = visual.Rect(win, pos=(0, bar_y), lineColor=None, fillColor='white', width=0.01, height=0.4)
        bar_frame = visual.Rect(win, pos=(0, bar_y), lineColor='white', fillColor=None, width=1.9, height=0.2)

        # Display all
        img_stim.draw()
        progress_bar.draw()
        center_line.draw()
        bar_frame.draw()
        win.flip()

        # Debug
        event.waitKeys()
