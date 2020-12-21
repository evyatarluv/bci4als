"""

Each function get the subject's folder path and return a dict.
The dict include key for each day while the value for each day is also a dict.
The dict for each day include train & test ndarray.

"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

data_params = {
    'filename': {'y': 'stimulus_vector.csv', 'X': 'noam_name.csv'}
}

same_day_params = {
    'train_ratio': 0.8,
    'random_state': 42,
}

adjust_params = {
    'train_ratio': {'first': 0.8, 'others': 0.1},
    'random_state': 42,
}


def same_day_data(subject_folder):
    """
    This function get the subject's folder directory and return a dict with train and test for each day.
    In `same_day` mode the model train and test himself on the same day.
    :param subject_folder: str, path to the subject's folder
    :return: dict with train & test for each day.
    """

    days = os.listdir(subject_folder)
    train_test = {}

    for d in days:
        # Get current day path
        day_path = os.path.join(subject_folder, d)

        # Load X & y
        y = pd.read_csv(os.path.join(day_path, data_params['filename']['y']))
        X = pd.read_csv(os.path.join(day_path, data_params['filename']['X']))

        # Split
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            train_size=same_day_params['train_ratio'],
                                                            random_state=same_day_params['random_state'])

        # Update the dict
        train_test[d] = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}

    return train_test


def first_day_data(subject_folder):
    """
    In 'first_day' mode the model train only on the first day and test on the other days.
    :param subject_folder: str, path to the subject's folder
    :return: dict, train & test for each day
    """

    days = os.listdir(subject_folder)
    train_test = {}

    for d in days:

        # Get current day path
        day_path = os.path.join(subject_folder, d)

        # Load X & y
        y = pd.read_csv(os.path.join(day_path, data_params['filename']['y']))
        X = pd.read_csv(os.path.join(day_path, data_params['filename']['X']))

        # If this is day 1 split to train and test
        if d == '1':
            X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                                train_size=same_day_params['train_ratio'],
                                                                random_state=same_day_params['random_state'])

            train_test[d] = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}

        # Otherwise train using the first day and test on the current day
        else:

            train_test[d] = {'X_train': train_test['1']['X_train'], 'X_test': X,
                             'y_train': train_test['1']['y_train'], 'y_test': y}

    return train_test


def adjust_data(subject_folder):
    """
    In 'adjust' mode the model trains on the first day and on couple of trials from the current day.
    Then the model test on the rest of the samples from the current day.
    :param subject_folder: str, path to the subject's folder
    :return: dict with train & test for each day.
    """

    days = os.listdir(subject_folder)
    train_test = {}

    for d in days:

        # Get current day path
        day_path = os.path.join(subject_folder, d)

        # Load X & y
        y = pd.read_csv(os.path.join(day_path, data_params['filename']['y']))
        X = pd.read_csv(os.path.join(day_path, data_params['filename']['X']))

        # If this is day 1 split to train and test
        if d == '1':
            X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                                train_size=adjust_params['train_ratio']['first'],
                                                                random_state=same_day_params['random_state'])

            train_test[d] = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}

        # Otherwise split differently
        else:

            X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                                train_size=adjust_params['train_ratio']['others'],
                                                                random_state=adjust_params['random_state'])

            train_test[d] = {'X_train': np.concatenate((train_test['1']['X_train'], X_train)),
                             'X_test': X_test,
                             'y_train': np.concatenate((train_test['1']['y_train'], y_train)),
                             'y_test': y_test}

    return train_test


def train_model(X_train, y_train, model_name):
    """
    The function train model according to the model_name arg with the given data.
    :param X_train: ndarray, X train matrix
    :param y_train: ndarray, y train vector
    :param model_name: str, model to train
    :return: trained model
    """

    if model_name.lower() == 'svm':

        model = SVC()
        model.fit(X_train, y_train)

    # todo: raise NotImplementedError at the end

    return model


def MI5_learn_model(subject_folder, mode, model_name):

    switcher = {'same day': same_day_data, 'first day': first_day_data, 'adjust': adjust_data}

    # Get the data for the model
    try:
        training_data = switcher[mode.lower()](subject_folder)

    except KeyError:
        raise NotImplementedError('Not implemented mode, please choose different mode')

    # Train model and test it
    results = {}
    for day, data in training_data.items():

        X_train, X_test, y_train, y_test = data.values()

        # todo: scale?
        model = train_model(X_train, y_train, model_name)

        results[day] = model.score(X_test, y_test)

    print('Accuracy for each day using `{}` mode:'.format(mode))
    print('\n'.join('Day {}, Accuracy: {}'.format(k, v) for k, v in results.items()))
