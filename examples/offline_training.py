import pickle
from time import strftime
from typing import List

from mne.io import RawArray
import mne
import pandas as pd
from mne_features import feature_extraction
from bci4als.eeg import EEG
from bci4als.offline import OfflineExperiment
import numpy as np


def preprocess(eeg: EEG, trials: List[pd.DataFrame], ch_names: List[str]) -> List[RawArray]:

    filtered_trials = []

    for trial in trials:

        # Create MNE RawArray object
        eeg_data = trial.to_numpy() / 1000000  # BrainFlow returns uV, convert to V for MNE
        eeg_data = eeg_data.T  # Transpose for MNE
        ch_types = ['eeg'] * len(eeg_data)
        info = mne.create_info(ch_names=eeg.eeg_names, sfreq=eeg.sfreq, ch_types=ch_types)
        raw = RawArray(eeg_data, info).pick_channels(ch_names)

        # Filter the data
        raw = EEG.filter_data(raw, notch=50, low_pass=4, high_pass=48)

        # Append to the filtered list
        filtered_trials.append(raw)

    return filtered_trials


def to_3d_matrix(trials_ndarray: List[np.ndarray]):
    """
    Get list with ndarray and create 3d matrix for the given list.
    The dimensions of the matrix is: (n_rows, min(n_cols)).
    :param trials_ndarray: list with ndarray
    :return:
    """

    n_col = min(trials_ndarray, key=lambda x: x.shape[1]).shape[1]

    matrix = np.dstack(map(lambda x: x[:, :n_col], trials_ndarray))

    return np.rollaxis(matrix, -1)


def extract_features(eeg: EEG, trials: List[RawArray], features: List[str]) -> np.ndarray:

    # Convert RawArray to ndarray
    trials_ndarray = list(map(lambda x: x.get_data(), trials))

    # Convert to 3d matrix
    trials_ndarray = to_3d_matrix(trials_ndarray)

    # Return features
    return feature_extraction.extract_features(trials_ndarray, sfreq=eeg.sfreq, selected_funcs=features)


def train_model(features, labels):
    """
    Train a SGDClassifier model on the features and labels.
    Return the model.
    Args:
        features: ndarray[num_samples, num_features]
        labels: list[num_samples]. each entry is 0, 1 or 2

    Returns:

    """
    raise NotImplementedError


def main():

    eeg = EEG(board_id=2, ip_port=6677, serial_port="COM6")

    exp = OfflineExperiment(eeg=eeg, num_trials=4, trial_length=2)

    trials, labels = exp.run()

    # trials = preprocess(eeg, trials, ch_names=['C3', 'C4'])
    #
    # features = extract_features(eeg, trials, features=['ptp_amp', 'mean', 'skewness'])
    #
    # model = train_model(features, labels)
    #
    # filename = "saved_models/model-{}.pickle".format(strftime())
    # file = open(filename, 'wb')
    # pickle.dump(model, file)


if __name__ == '__main__':

    main()
