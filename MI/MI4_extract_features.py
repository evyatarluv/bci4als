import json
import os
import pickle

import cv2
import matplotlib.pyplot as plt
import mne_features
import numpy as np
# from keras.applications import resnet_v2
from scipy.signal import welch

from MI.MI3_segment_data import data_params as MI3_params

data_params = {
    'record_folder': r'C:\Users\noam\PycharmProjects\BCI-4-ALS2\data\evyatar',
    # path to the subject folder with all the recording folders
    'features_filename': 'features.csv'
}

features_params = {
    'selected_channel': ['C03', 'C04'],
    'nfft': 512,
    'welch_window': 'hamm',
    'trial_time': 5,  # seconds
    'image_size': (500, 32),
}


def extract_features(trials, s_freq):
    """
    The function gets list of m trials, and extracts k features (scalar values) per trial.
    :param trials: list of trials while each trial is a pandas dataframe
    :return: ndarray of extracted features [shape = (m_trials, k_features)].
    """
    # initialize

    # transform list of trials into X: ndarray, shape (n_trials, n_channels, n_times)
    trials = [trial[features_params['selected_channel']].to_numpy() for trial in trials]  # convert to numpy
    n_times = min(trials, key=lambda x: x.shape[0]).shape[0]  # get minimum trial length
    trials = [trial[:n_times].T for trial in trials]  # trim trials to minimum length
    X = np.stack(trials)
    params = {
        'pow_freq_bands__freq_bands': np.arange(1, int(s_freq / 2), 1),
    }
    selected_funcs = {'mean', 'ptp_amp', 'std', 'pow_freq_bands'}
    features_array = mne_features.feature_extraction.extract_features(X, s_freq, selected_funcs, params)

    return features_array

    # per-trial feature extraction
    for trial in trials:
        trial_features_lst = []

        # 1) extract power spectrum density (via welch method)
        sample_rate = len(trial.index) / features_params['trial_time']  # Units: 1/s
        nfft = features_params['nfft']
        welch_window = features_params['welch_window']
        channel = features_params['selected_channel']  # todo: tweak this hyper-parameter
        trial_features_lst.append(welch(trial[channel], window=welch_window, fs=sample_rate, nfft=nfft)[1])

        # 2) Use ResNet to extract some features
        if False:
            resized_trial = cv2.resize(trial, features_params['image_size'])
            plt.imshow(resized_trial)
            plt.show()
            input('IMAGE')
            resized_trial = cv2.merge((resized_trial, resized_trial, resized_trial))
            resnet = resnet_v2.ResNet50V2(include_top=False)

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
        info_path = os.path.join(subject_path, '.info')
        trials = pickle.load(open(trials_path, 'rb'))
        s_freq = json.load(open(info_path, 'r'))['effective_srate']

        # Extract features from each trial
        print("Extracting Features for subject: {}".format(subject_path))

        features = extract_features(trials, s_freq)

        # Save the features
        features_path = os.path.join(subject_path, data_params['features_filename'])
        print("Saving features to: {}".format(features_path))
        np.savetxt(features_path, features, delimiter=',')


if __name__ == '__main__':
    MI_extract_features()
