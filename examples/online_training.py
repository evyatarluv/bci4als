import pickle
from typing import List, Tuple

import numpy as np
from psychopy import visual, event
from bci4als.learning.online import Feedback, OnlineExperiment
from bci4als.learning.eeg import EEG

# Check the feedback
def check_feedback():
    win = visual.Window(fullscr=False)
    f = Feedback(win, 1)
    f.update(1)
    event.waitKeys()
    f.update(1)
    event.waitKeys()

# Extract data from board data

# Load
# data = pickle.load(open('board_data/data.pickle', 'rb'))
# marker_row = 31
#
# # Get markers
# markers_idx = np.where(data[marker_row, :] != 0)[0]
#
# # Get labels and durations list from the markers
# labels: List[int] = []
# durations: List[Tuple] = []
# for time in markers_idx:
#
#     status, label, index = EEG.decode_marker(data[marker_row, time])
#
#     if status == 'start':
#
#         labels.append(label)
#         durations.append((time, ))
#
#     elif status == 'stop':
#
#         durations[-1] = durations[-1] + (time, )
#
# print(labels)
# print(durations)

def run_experiment():

    eeg = EEG(board_id=2, ip_port=6677, serial_port="COM4")

    exp = OnlineExperiment(eeg=eeg, num_trials=3, buffer_time=5, threshold=3)
    exp.run(use_eeg=False)


if __name__ == '__main__':
    run_experiment()

