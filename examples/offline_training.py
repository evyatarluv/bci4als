import pickle
from typing import List
import mne
import pandas as pd
from bci4als.eeg import EEG
from bci4als.ml_model import MLModel
from bci4als.experiments.offline import OfflineExperiment
import numpy as np
from mne_features.feature_extraction import extract_features
from sklearn.preprocessing import StandardScaler


def laplacian(data, channels: List[str]):
    """
    The method execute laplacian on the raw data.
    The laplacian was computed as follows:
        1. C3 = C3 - mean(Cz + F3 + P3 + T3)
        2. C4 = C4 - mean(Cz + F4 + P4 + T4)
    :return:
    """

    # Dict with all the indices of the channels
    idx = {ch: channels.index(ch) for ch in channels}

    # C3
    data[idx['C3']] -= (data[idx['Cz']] + data[idx['FC5']] + data[idx['FC1']] +
                        data[idx['CP5']] + data[idx['CP1']]) / 5

    # C4
    data[idx['C4']] -= (data[idx['Cz']] + data[idx['FC2']] + data[idx['FC6']] +
                        data[idx['CP2']] + data[idx['CP6']]) / 5

    return data[[idx['C3'], idx['C4']]]


def preprocess(eeg: EEG, trials: List[pd.DataFrame]) -> List[np.ndarray]:
    """
    Preprocess the EEG data, including the following steps:
        1. filters
        2. laplacian
        3. normalization
    :param eeg:
    :param trials:
    :return:
    """
    filtered_trials = []

    for trial in trials:
        # Get the data as a numpy array
        data = trial.values

        # Convert to MNE props
        data = data.astype(np.float64).T

        # Band-pass & notch filters
        data = mne.filter.filter_data(data, l_freq=8, h_freq=30, sfreq=eeg.sfreq, verbose=False)
        # data = mne.filter.notch_filter(data, Fs=eeg.sfreq, freqs=50, verbose=False)

        # Laplacian
        data = laplacian(data, eeg.get_board_names())

        # Normalize
        scaler = StandardScaler()
        data = scaler.fit_transform(data.T)

        # Append to the filtered list
        filtered_trials.append(data)

    return filtered_trials


def get_features(eeg: EEG, trials: List[np.ndarray]) -> List[np.ndarray]:
    # Features extraction
    funcs_params = {'pow_freq_bands__freq_bands': np.array([8, 10, 12.5, 30])}
    selected_funcs = ['pow_freq_bands', 'variance']
    X = [extract_features(x.T[np.newaxis], eeg.sfreq, selected_funcs, funcs_params)[0] for x in trials]

    return X


def offline_experiment(run: bool = True, path: str = None):

    eeg = EEG(board_id=2)

    exp = OfflineExperiment(eeg=eeg, num_trials=1, trial_length=3,
                            full_screen=False, audio=False)

    if run:
        trials, labels = exp.run()
    else:
        trials = pickle.load(open(path.format('trials.pickle'), 'rb'))
        labels = [int(i) for i in np.genfromtxt(path.format('labels.csv'), delimiter=',')]

    # Classification
    model = MLModel()
    session_directory = exp.session_directory if run else path
    model.offline_training(eeg=eeg, trials=trials, labels=labels,
                           subject_folder=session_directory, model_type='csp_lda')


if __name__ == '__main__':

    offline_experiment(run=True, path='../recordings/adi/7/{}')

