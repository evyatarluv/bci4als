import os
import pickle
from MI.MI3_segment_data import data_params as MI3_params

data_params = {
    'record_folder': 'C:\\Users\\lenovo\\Documents\\CurrentStudy',  # path to the folder with all the subjects
    'features_filename': 'features.pickle'
}

features_params = {

}


def extract_features(trials):

    """
    The function get list of trials and return list of features for each trial.
    :param trials: list of trials while each trial is a pandas dataframe
    :return: list of features for each trial, each feature is a list of values
    """
    # todo: write this function
    pass


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
        features = extract_features(trials)

        # Dump the features
        features_path = os.path.join(subject_path, data_params['features_filename'])
        pickle.dump(features, open(features_path, 'wb'))


if __name__ == '__main__':

    MI_extract_features()