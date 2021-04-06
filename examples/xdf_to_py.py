import os
from typing import List, Tuple
from nptyping import NDArray
import mne
import numpy as np
import pyxdf
import pickle


class EEG:

    def __init__(self, xdf_path: str, channels: List[str]):

        self.channels: List[str] = channels
        self.labels: List[int] = []
        self.sample_freq: float = 125
        self._xdf, _ = pyxdf.load_xdf(xdf_path)
        self.data: NDArray = self._xdf[1]['time_series'][:, 3:]  # remove first 3 columns (time, noisy, noisy)
        self.duration: List[Tuple] = self.extract_durations()

    def extract_durations(self) -> List[Tuple]:
        """
        The method extract from the xdf raw data the duration of each trial.
        The durations are saved as list of tuples were each tuple constructed as (start, end)
        :return:
        """
        # Markers which used for start & end
        START_TRIAL = 1111
        END_TRIAL = 9
        START_RECORD = 111
        END_RECORD = 99

        # Get relevant data from the xdf
        data_timestamps = self._xdf[1]['time_stamps']
        markers_timestamps = self._xdf[0]['time_stamps']
        markers = self._xdf[0]['time_series']

        # Create the durations list
        durations = []
        for ts, m in zip(markers_timestamps, markers):

            m = float(m[0])  # convert marker to float

            # Skip un-relevant markers
            if m in [START_RECORD, END_RECORD]:
                continue

            # Start trial marker
            if m == START_TRIAL:

                idx = np.argmin(data_timestamps < ts)
                durations.append((idx,))

            # End trial marker
            elif m == END_TRIAL:

                idx = np.argmin(data_timestamps < ts)
                durations[-1] += (idx,)

            # Label marker
            else:

                self.labels.append(int(m))

        return durations

    def laplacian(self):
        """
        The method execute laplacian on the raw data.
        The laplacian was computed as follows:
            1. C3 = C3 - mean(Cz + F3 + P3 + T3)
            2. C4 = C4 - mean(Cz + F4 + P4 + T4)
        :return:
        """

        # Dict with all the indices of the channels
        idx = {ch: self.channels.index(ch) for ch in self.channels}

        # C3
        self.data[idx['C3']] -= (self.data[idx['Cz']] + self.data[idx['FC5']] + self.data[idx['FC1']] +
                                 self.data[idx['CP5']] + self.data[idx['CP1']]) / 4

        # C4
        self.data[idx['C4']] -= (self.data[idx['Cz']] + self.data[idx['FC2']] + self.data[idx['FC6']] +
                                 self.data[idx['CP2']] + self.data[idx['CP6']]) / 4

    def filter(self, low_pass: float, high_pass: float, notch: float):
        """
        Filter the EEG data
        :param low_pass:
        :param high_pass:
        :param notch:
        :return:
        """
        # Convert to MNE props
        self.data = self.data.astype(np.float64)
        self.data = self.data.T

        # Low pass
        self.data = mne.filter.filter_data(self.data, l_freq=None, h_freq=low_pass, sfreq=self.sample_freq)

        # High pass
        self.data = mne.filter.filter_data(self.data, l_freq=high_pass, h_freq=None, sfreq=self.sample_freq)

        # Notch
        self.data = mne.filter.notch_filter(self.data, Fs=self.sample_freq, freqs=notch)

        # Return to normal
        self.data = self.data.T

    def split_trials(self) -> [NDArray, NDArray, NDArray]:
        """
        The method split the EEG data into 3d matrices, a matrix for each label.
        :return: 3d matrices in the following order: idle, left, right
        """
        n_samples = min([d[1] - d[0] for d in self.duration])
        idles, lefts, rights = [], [], []

        for idx, duration in enumerate(self.duration):

            trial = self.data[duration[0]:duration[0] + n_samples]
            label = self.labels[idx]

            if label == 1:
                idles.append(trial)

            elif label == 2:
                lefts.append(trial)

            elif label == 3:
                rights.append(trial)

            else:
                raise ValueError('Un-recognized label')

        # Stack as 3d matrix
        idles, lefts, rights = np.dstack(idles), np.dstack(lefts), np.dstack(rights)

        return np.rollaxis(idles, -1), np.rollaxis(lefts, -1), np.rollaxis(rights, -1)


ch_names = ['C03', 'C04', 'P07', 'P08', 'O01', 'O02', 'F07', 'F08', 'F03', 'F04', 'T07', 'T08', 'P03']
data_folder = 'adi_eden_records'
filename = 'EEG.xdf'

for sub in os.listdir(data_folder):

    eeg = EEG(os.path.join(data_folder, sub, filename), ch_names)  # read the data
    pickle_dict = {'data': eeg.data, 'duration': eeg.duration, 'ch_names': eeg.channels, 'labels': eeg.labels}
    pickle_name = '{}.pkl'.format(sub)
    pickle.dump(pickle_dict, open(pickle_name, 'wb'))



