import os
import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.applications import resnet_v2
from sklearn.decomposition import PCA

image_size = (100, 600)

resnet = resnet_v2.ResNet50V2(include_top=False, weights='imagenet', pooling='avg',
                              input_shape=image_size[::-1] + (3,))
# Get the current subject trials
subject_path = os.path.join('..\\data\\evyatar', '1')
trials_path = os.path.join(subject_path, 'EEG_trials.pickle')
trials = pickle.load(open(trials_path, 'rb'))


def extract_features_resnet(trials, cnn):

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
        resized_trial = cv2.resize(trial.to_numpy(), image_size)
        resized_trial = cv2.merge((resized_trial, resized_trial, resized_trial))

        # Append resized trial
        resized_trials.append(resized_trial)

    resized_trials = np.stack(resized_trials)

    features = cnn.predict(resized_trials)

    # Use PCA for dimensionality reduction
    pca = PCA(n_components=100)
    features = pca.fit_transform(features)

    return features


f = extract_features_resnet(trials, resnet)
