"""

Each function get the subject's folder path and return a dict.
The dict include key for each day while the value for each day is also a dict.
The dict for each day include train & test ndarray.

"""
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import numpy as np
from .. import params


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
        y = np.genfromtxt(os.path.join(day_path, params['data']['filenames']['y']), delimiter=',')
        X = np.genfromtxt(os.path.join(day_path, params['data']['filenames']['features']), delimiter=',')

        # Split
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            train_size=params['split']['adjust']['train_ratio'],
                                                            random_state=params['split']['random_state'])

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
        y = np.genfromtxt(os.path.join(day_path, params['data']['filenames']['y']), delimiter=',')
        X = np.genfromtxt(os.path.join(day_path, params['data']['filenames']['features']), delimiter=',')

        # If this is day 1 split to train and test
        if d == '1':
            X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                                train_size=params['split']['same_day']['train_ratio'],
                                                                random_state=params['split']['random_state'])

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
        y = np.genfromtxt(os.path.join(day_path, params['data']['filenames']['y']), delimiter=',')
        X = np.genfromtxt(os.path.join(day_path, params['data']['filenames']['features']), delimiter=',')

        # If this is day 1 split to train and test
        if d == '1':
            X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                                train_size=params['split']['adjust']['train_ratio'][
                                                                    'first'],
                                                                random_state=params['split']['random_state'])

            train_test[d] = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}

        # Otherwise split differently
        else:

            X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                                train_size=params['split']['adjust']['train_ratio'][
                                                                    'others'],
                                                                random_state=params['split']['random_state'])

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

    # SVM
    if model_name.lower() == 'svm':
        model = SVC(C=2, gamma='auto')

    # KNN
    elif model_name.lower() == 'knn':
        model = KNeighborsClassifier(n_neighbors=10)

    # Random Forest
    elif model_name.lower() in ['rf', 'random_forest']:
        model = RandomForestClassifier(n_estimators=250)

    else:
        raise NotImplementedError('The chosen model is not implemented yet')

    model.fit(X_train, y_train)

    return model


def train(mode='same day', model_name='svm'):

    print('---------- Start MI5 - Training Model ----------')

    subject_folder = params['data']['subject_folder']
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

        scaler_x = StandardScaler()
        X_train = scaler_x.fit_transform(X_train)

        model = train_model(X_train, y_train, model_name)

        print('Day {} predictions: {}'.format(day, model.predict(scaler_x.transform(X_test))))
        results[day] = round(model.score(scaler_x.transform(X_test), y_test), 3)

    print('Accuracy for each day using `{}` mode and {} model:'.format(mode, model_name))
    print('\n'.join('Day {}, Accuracy: {}'.format(k, v) for k, v in results.items()))


if __name__ == '__main__':
    train()
