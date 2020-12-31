import mne
import pyxdf
import os
import numpy as np
from pyprep import PrepPipeline

path = '../data/evyatar/3'

# import XDF
markers, _ = pyxdf.load_xdf(os.path.join(path, 'EEG.xdf'), [{'type': 'Markers'}])
data, header = pyxdf.load_xdf(os.path.join(path, 'EEG.xdf'), [{'type': 'EEG'}])
eeg = np.delete(data[0]['time_series'], 0, 1)
s_rate = data[0]['info']['effective_srate']
start_time = markers[0]['time_stamps'][0] - data[0]['time_stamps'][0]
ch_names = ['Fp1', 'Fp2', 'C03', 'C04', 'P07', 'P08', 'O01', 'O02',
            'F07', 'F08', 'F03', 'F04', 'T07', 'T08', 'P03']

# create mne raw data
info = mne.create_info(ch_names, s_rate)
eeg_raw = mne.io.RawArray(eeg.T, info, first_samp=start_time * s_rate)

# Inspect
prep = PrepPipeline(eeg_raw, montage='standard_1005')
prep.fit()
print("Bad channels: {}".format(prep.interpolated_channels))