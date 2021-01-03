import mne
import pyxdf
import os
import numpy as np
import pandas as pd

path = '../data/noam/2'

# ----------------------------------------- EEG.xdf -------------------------------------
# import XDF
markers, _ = pyxdf.load_xdf(os.path.join(path, 'EEG.xdf'), [{'type': 'Markers'}])
data, header = pyxdf.load_xdf(os.path.join(path, 'EEG.xdf'), [{'type': 'EEG'}])
eeg = np.delete(data[0]['time_series'], 0, 1)
s_rate = data[0]['info']['effective_srate']
start_time = markers[0]['time_stamps'][0] - data[0]['time_stamps'][0]
ch_names = ['Fp1', 'Fp2', 'C03', 'C04', 'P07', 'P08', 'O01', 'O02',
            'F07', 'F08', 'F03', 'F04', 'T07', 'T08', 'P03']

# create mne raw data
info = mne.create_info(ch_names, s_rate, ch_types='eeg')
eeg_raw = mne.io.RawArray(eeg.T, info, first_samp=start_time * s_rate)

# Filter
eeg_raw.notch_filter(freqs=50, picks=ch_names)
eeg_raw.filter(l_freq=0.5, h_freq=None, picks=ch_names)
eeg_raw.filter(l_freq=None, h_freq=30, picks=ch_names)

# ICA
ica = mne.preprocessing.ICA(n_components=15, random_state=97)
ica.fit(eeg_raw, picks=ch_names)
ica.apply(eeg_raw)

eeg_raw.set_channel_types({i: 'eeg' for i in ch_names})
eeg_raw.plot()

# --------------------------------------- Clean EEG --------------------------------------------
# eeg = pd.read_csv(os.path.join(path, 'EEG_clean.csv')).drop('time', axis=1)
# ch_names = list(eeg.columns)
# eeg = eeg.to_numpy()
# s_rate = pyxdf.load_xdf(os.path.join(path, 'EEG.xdf'), [{'type': 'EEG'}])[0][0]['info']['effective_srate']
#
# info = mne.create_info(ch_names, s_rate)
# eeg_raw = mne.io.RawArray(eeg.T, info)
# eeg_raw.plot()

