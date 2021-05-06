import pickle
from typing import List, Tuple

import numpy as np
from bci4als.ml_model import MLModel
from psychopy import visual, event
from bci4als.online import Feedback, OnlineExperiment
from bci4als.eeg import EEG


def run_experiment(model_path: str):

    model = MLModel(model_path=model_path)

    eeg = EEG(board_id=-1)

    exp = OnlineExperiment(eeg=eeg, model=model, num_trials=25, buffer_time=4, threshold=3)

    exp.run(use_eeg=True, full_screen=False)

    # exp.warmup(use_eeg=True, target='right')


if __name__ == '__main__':

    run_experiment(model_path=r'C:\Users\lenovo\Desktop\1\model.pickle')

