import pickle
import numpy as np
import pyxdf
import mne
import os

data_path = '../data/noam/2'
trial = 50
eeg_path = os.path.join(data_path, 'EEG.xdf')
trials_path = os.path.join(data_path, 'EEG_trials.pickle')
ch_names = ['C03', 'C04', 'P07', 'P089', 'O01', 'O02', 'F07', 'F08', 'F03', 'F04', 'T07', 'T08', 'P03']
s_rate = 125

trials = pickle.load(open(trials_path, 'rb'))
trial_data = trials[trial].to_numpy()
full_data = pyxdf.load_xdf(eeg_path, [{'type': 'EEG'}])[0][0]['time_series'][:, 3:]

info = mne.create_info(ch_names, s_rate)
raw_trial = mne.io.RawArray(trial_data.T, info)
raw_full_data = mne.io.RawArray(full_data.T, info)


# raw_trial.plot(n_channels=2)
# raw_trial.plot_psd(picks=['C03', 'C04'])
raw_full_data.plot_psd(picks=['C03', 'C04'])
