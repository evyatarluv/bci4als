import pickle
from typing import List, Tuple

import numpy as np
from psychopy import visual, event
from bci4als.online import Feedback, OnlineExperiment
from bci4als.eeg import EEG


def run_experiment():

    model = pickle.load(open(r'models/7/MultinomialNB.pkl', 'rb'))

    eeg = EEG(board_id=2, ip_port=6677, serial_port="COM6")

    exp = OnlineExperiment(eeg=eeg, model=model, num_trials=25, buffer_time=4, threshold=3)

    exp.run(use_eeg=True)

    # exp.warmup(use_eeg=True, target='right')


if __name__ == '__main__':

    run_experiment()

