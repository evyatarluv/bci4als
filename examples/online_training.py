import pickle
from typing import List, Tuple

import numpy as np
from psychopy import visual, event
from bci4als.online import Feedback, OnlineExperiment
from bci4als.eeg import EEG

def run_experiment():

    eeg = EEG(board_id=2, ip_port=6677, serial_port="COM4")

    exp = OnlineExperiment(eeg=eeg, model=None, num_trials=3, buffer_time=3, threshold=3)

    exp.run(use_eeg=False)


if __name__ == '__main__':
    run_experiment()

