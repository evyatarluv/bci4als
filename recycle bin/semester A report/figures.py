import pickle
import numpy as np
import pyxdf
import mne
import os
import matplotlib.pyplot as plt

data_path = '../bci4als/data/noam/2'
trial = 50
eeg_path = os.path.join(data_path, 'EEG.xdf')
trials_path = os.path.join(data_path, 'EEG_trials.pickle')
clean_path = os.path.join(data_path, 'EEG_clean.csv')
ch_names = ['C03', 'C04', 'P07', 'P089', 'O01', 'O02', 'F07', 'F08', 'F03', 'F04', 'T07', 'T08', 'P03']
s_rate = 125

trials = pickle.load(open(trials_path, 'rb'))
trial_data = trials[trial].to_numpy()
full_data = pyxdf.load_xdf(eeg_path, [{'type': 'EEG'}])[0][0]['time_series'][:, 3:]
clean_data = np.genfromtxt(clean_path, delimiter=',', skip_header=1)[:, 1:]

info = mne.create_info(ch_names, s_rate, verbose=False)
raw_trial = mne.io.RawArray(trial_data.T, info, verbose=False)
raw_full_data = mne.io.RawArray(full_data.T, info, verbose=False)
raw_clean_data = mne.io.RawArray(clean_data.T, info, verbose=False)


raw_trial.plot()
# raw_trial.plot_psd(picks=ch_names)
# fig_1 = raw_full_data.plot_psd(picks=ch_names)
# fig_2 = raw_clean_data.plot_psd(picks=ch_names)
