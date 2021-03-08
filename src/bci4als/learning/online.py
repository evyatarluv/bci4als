import random
import threading
import time
from typing import Dict, List
from bci4als.learning.eeg import EEG
from bci4als.learning.experiment import Experiment
from psychopy import visual, core
from sklearn.linear_model import SGDClassifier


class OnlineExperiment(Experiment):
    """
    Class for running an online MI experiment.

    Attributes:
    ----------

        num_trials (int):
            Amount of trials in the experiment.

        buffer_time (float):
            Time in seconds for collecting EEG data before model's prediction.

        threshold (int):
            The amount the times the model need to be correct (predict = stim) before moving to the next stim.

    """

    def __init__(self, eeg: EEG, model: SGDClassifier, num_trials: int,
                 buffer_time: float, threshold: int):

        super().__init__(eeg, num_trials)
        self.threshold: int = threshold
        self.buffer_time: float = buffer_time
        self.trials = self._init_trials()
        # Init psychopy window
        self.win = visual.Window(monitor='testMonitor', fullscr=False)
        self.model = model

    def _init_trials(self) -> List[int]:
        """
        Create list with trials as num_trials attributes.
        The trials consists of equal number of right and left targets (0, 1).
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

    def _learning_model(self, feedback: Feedback):

        """
        The method for learning the model from the current stim.

        A separate thread runs this method. The method responsible for the following steps:
            1. Collecting the EEG data from the board (according to the buffer time attribute).
            2. Predicting the stim using the current model and collected EEG data.
            3. Updating the feedback object according to the model's prediction.
            4. Updating the model according to the data and stim.

        :param feedback: feedback visualization for the subject
        :return:
        """

        timer = core.Clock()

        while not feedback.confident:

            # Sleep until the buffer full
            time.sleep(max(0, self.buffer_time - timer.getTime()))

            # Get the data
            features = self.eeg.get_features()

            # Reset the clock for the next buffer
            timer.reset()

            # Predict using the subject EEG data
            prediction = self.model.predict(features)

            # Update the feedback according the prediction
            feedback.update(prediction)

            # Update the model using partial-fit with the new EEG data
            # todo: this assumes learning after every attempt. Consider alternatives.
            # todo: add y label to the fit method (add current label attribute)
            self.model.partial_fit(features)

        print('Finished learning model')

    def run(self, use_eeg: bool = True):

        # turn on EEG streaming
        if use_eeg:
            self.eeg.on()

        # For each stim in the trials list
        for stim in self.trials:

            # Init feedback instance
            feedback = Feedback(self.win, stim, self.buffer_time, self.threshold)

            # Use different thread for online learning of the model
            threading.Thread(target=self._learning_model, args=(feedback,)).start()

            # Maintain visual feedback on screen
            timer = core.Clock()

            while not feedback.confident:

                feedback.display(current_time=timer.getTime())

                # Reset the timer according the buffer time attribute
                if timer.getTime() > self.buffer_time:
                    timer.reset()

            # Waiting for key-press between trials
            self._wait_between_trials(feedback, self.eeg, use_eeg)

        # turn off EEG streaming
        if use_eeg:
            self.eeg.off()
