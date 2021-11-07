import os
import time
from collections import namedtuple
from typing import Dict
from psychopy import visual

# name tuple object for the progress bar params
Bar = namedtuple('Bar', ['pos', 'line_size', 'frame_size', 'frame_color', 'fill_color'])

from zmq import Socket, Context, PUB


class FeedbackUnity:
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

    ADDRESS = '127.0.0.1'
    PORT = 5555

    def __init__(self, buffer_time: float, threshold: int = 3, refresh_rate: float = 0.1):

        self.stim: int = None
        self.stop = False
        self.refresh_rate: float = refresh_rate
        self.buffer_time: float = buffer_time

        self._target_updated = False
        ctx = Context()
        self.socket = ctx.socket(PUB)
        self.socket.bind(f'tcp://{self.ADDRESS}:{self.PORT}')

        # Images params
        self.enum_image = {0: 'right', 1: 'left', 2: 'idle', 3: 'tongue', 4: 'legs'}

    def set_stimulation(self, stim: int):
        self.stop = False
        self.stim = int(stim)

    def update(self, predict_stim: int, predict_confidence: float, skip: bool = False):
        """
        Update the feedback on screen.
        The update occur according to the model prediction. If the model was right
        the progress bar get wider, otherwise it stay the same size.
        :param predict_stim: prediction of the model.
        :param skip: optionally skip this stimulus.
        :return:
        """
        predict_stim = int(predict_stim)
        predict_confidence = predict_confidence
        message = {'type': 'PREDICT', 'message': predict_stim, 'confidence': predict_confidence}
        print(f'Sending message - "{message}"')
        self.socket.send_json(message)
        self._target_updated = False
        # If the model predicted right
        if predict_stim == self.stim:
            self.stop = True
        if skip:
            self.stop = True

    def display(self, current_time: float):
        """
        Display the current state of the progress bar aside to the current stim
        :param current_time: the current time for the time bar object
        :return:
        """
        if not self._target_updated:
            message = {'type': 'TARGET', 'message': self.stim, 'interval': self.buffer_time}
            print(f'Sending message - "{message}"')
            self.socket.send_json(message)
            self._target_updated = True

        time.sleep(self.refresh_rate)

    def end_trial(self):
        time.sleep(2)

    def close(self):
        self.socket.close()
