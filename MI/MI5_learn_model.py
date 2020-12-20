"""

Each function get the subject's folder path and return a dict.
The dict include key for each day while the value for each day is also a dict.
The dict for each day include train & test ndarray.

"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

data_params = {
    'filename': {'y': 'stimulus_vector.csv', 'X': 'noam_name.csv'}
}

switcher = {
    'same_day': 4,
    'adjust': 5,
    'first_day': 6
}

same_day_params = {
    'train_ratio': 0.8,
    'random_state': 42,
}


def same_day_training(subject_folder):

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


def first_day_training(subject_folder):

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

        # Otherwise use all data for test
        else:

            train_test[d] = {'X_test': X, 'y_test': y}

    return train_test


