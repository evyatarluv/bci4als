import pickle
import numpy as np
import pyxdf
import mne
import os

data_path = '../data/evyatar/3'
eeg_path = os.path.join(data_path, 'EEG.xdf')
trials_path = os.path.join(data_path, 'EEG_trials.pickle')
data = pyxdf.load_xdf(eeg_path, [{'type': 'EEG'}])[0][0]['time_series']
data = np.delete(data, [0], axis=1)

trials = pickle.load(open(trials_path, 'rb'))
data = trials[12].to_numpy()
ch_names = ['C03', 'C04', 'P07', 'P089', 'O01', 'O02', 'F07', 'F08', 'F03', 'F04', 'T07', 'T08', 'P03']
# data = data[:, 3:5]
# ch_names = ['C03', 'C04']
s_rate = 125

info = mne.create_info(ch_names, s_rate, ch_types=['eeg'] * len(ch_names))
raw_data = mne.io.RawArray(data.T, info)

raw_data.plot_psd(picks=['C03', 'C04'])
