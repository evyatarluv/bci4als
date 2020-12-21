import os
import pickle
import numpy as np
from scipy.signal import welch

from MI.MI3_segment_data import data_params as MI3_params

data_params = {
    'record_folder': r'C:\Users\noam\PycharmProjects\BCI-4-ALS\data\evyatar',  # path to the folder with all the subjects
    'features_filename': 'features.csv'
}

features_params = {
    'selected_channel': 'O01',
    'nfft': 512,
    'welch_window': 'hamm',
    'trial_time': 5  # seconds
}


def extract_features(trials):
    """
    The function gets list of m trials, and extracts k features (scalar values) per trial.
    :param trials: list of trials while each trial is a pandas dataframe
    :return: ndarray of extracted features [shape = (m_trials, k_features)].
    """
    # initialize
    features = []

    # per-trial feature extraction
    for trial in trials:
        trial_features_lst = []

        # 1) extract power spectrum density (via welch method)
        sample_rate = len(trial) / features_params['trial_time']  # Units: 1/s
        nfft = features_params['nfft']
        welch_window = features_params['welch_window']
        channel = features_params['selected_channel']  # todo: tweak this hyper-parameter
        trial_features_lst.append(welch(trial[channel], window=welch_window, fs=sample_rate, nfft=nfft)[1])

        # todo: add more feature extraction methods

        # concatenate all features to one array
        trial_features_vector = np.concatenate(trial_features_lst)

        # add features to list
        features.append(trial_features_vector)

    features_array = np.vstack(features)
    return features_array


def MI_extract_features():
    # Get all the subjects' folders
    subjects = os.listdir(data_params['record_folder'])

    # For each subject extract features
    for s in subjects:
        # Get the current subject trials
        subject_path = os.path.join(data_params['record_folder'], s)
        trials_path = os.path.join(subject_path, MI3_params['trials_filename'])
        trials = pickle.load(open(trials_path, 'rb'))

        # Extract features from each trial
        print("Extracting Features for subject: {}".format(subject_path))
        features = extract_features(trials)

        # Dump the features
        # todo: treat the output of extract_features function as ndarray
        features_path = os.path.join(subject_path, data_params['features_filename'])
        print("Saving features to: {}".format(features_path))
        np.savetxt(features_path, features, delimiter=',')


if __name__ == '__main__':
    MI_extract_features()
