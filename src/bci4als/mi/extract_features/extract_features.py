import json
import os
import pickle

import cv2
import mne_features
import numpy as np
from keras.applications import resnet_v2
from sklearn.decomposition import PCA

from .. import params


def extract_features_classic(trials, s_freq):
    """
    The function gets list of trials, and extracts classic ML features (scalar values) per trial.
    :param trials: list of trials while each trial is a pandas dataframe
    :param s_freq: float, sample frequency of the EEG data
    :return: ndarray of extracted features [shape = (m_trials, k_features)].
    """

    # Filter selected channels
    # Convert to ndarray X [shape = (n_trials, n_channels, n_times)]
    trials = [trial[params['features']['selected_channels']].to_numpy() for trial in trials]  # convert to numpy
    n_times = min(trials, key=lambda x: x.shape[0]).shape[0]  # get minimum trial length
    trials = [trial[:n_times].T for trial in trials]  # trim trials to minimum length
    X = np.stack(trials)

    # Features params for mne-features
    # https://mne.tools/mne-features/generated/mne_features.feature_extraction.FeatureExtractor.html

    mne_params = {
        'pow_freq_bands__freq_bands': np.arange(1, int(s_freq / 2), 1),
    }

    # Get features from mne_features
    features = mne_features.feature_extraction.extract_features(X, s_freq,
                                                                params['features']['features'],
                                                                mne_params)
    return features


def extract_features_cnn(trials, cnn):
    """
    The function get a list of n trials and CNN,
    and then uses the CNN to extract features from each trial.
    :param trials: list with n trial, where each trial is pandas DataFrame
    :param cnn: pre-trained CNN using keras.application
    :return: ndarray of features with shape (n_trials, m_features)
    """

    resized_trials = []

    for trial in trials:
        # Change image dimensions to fit the ResNet
        resized_trial = cv2.resize(trial.to_numpy(), params['features']['image_size'])
        resized_trial = cv2.merge((resized_trial, resized_trial, resized_trial))

        # Append resized trial
        resized_trials.append(resized_trial)

    resized_trials = np.stack(resized_trials)

    features = cnn.predict(resized_trials)

    # Use PCA for dimensionality reduction
    pca = PCA(n_components=params['features']['pca'])
    features = pca.fit_transform(features)

    return features


def extract_features(mode='classic'):
    print('---------- Start MI4 - Feature Extraction ----------')

    # Get all the subjects' folders
    days = os.listdir(params['data']['subject_folder'])

    if mode == 'cnn':
        cnn = resnet_v2.ResNet50V2(include_top=False, weights='imagenet', pooling='avg',
                                   input_shape=params['features']['image_size'][::-1] + (3,))
    else:
        cnn = None

    # For each day extract features
    for day in days:

        # Create paths for files
        day_path = os.path.join(params['data']['subject_folder'], day)
        trials_path = os.path.join(day_path, params['data']['filenames']['trials'])
        info_path = os.path.join(day_path, params['data']['filenames']['info'])

        # Get the current day trials & sample freq
        trials = pickle.load(open(trials_path, 'rb'))
        s_freq = json.load(open(info_path, 'r'))['effective_srate']

        # Extract features from each trial
        print("Extracting Features for subject: {}".format(day_path))

        if mode == 'cnn':
            features = extract_features_cnn(trials, cnn)
        else:
            features = extract_features_classic(trials, s_freq)

        # Save the features
        features_path = os.path.join(day_path, params['data']['filenames']['features'])
        print("Saving features to: {}".format(features_path))
        np.savetxt(features_path, features, delimiter=',')


if __name__ == '__main__':
    extract_features()
