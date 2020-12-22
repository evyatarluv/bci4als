import os
import numpy as np
import pandas as pd
import pyxdf
from MI.MI1_record_experiment import lsl_params
import pickle

data_params = {
    'record_folder': r'C:\Users\noam\PycharmProjects\BCI-4-ALS2\data\noam',  # path to the folder with all the subjects
    'EEG_filename': 'EEG_clean.csv',
    'trials_filename': 'EEG_trials.pickle',
}


def get_trials_times(subject_path):

    """
    This function get subject path and return a list of the trials timestamps.
    contains the trial'start & end timestamps.
    :param subject_path: str, path to the current subject folder
    :return: list with tuples correspond to the start & end of each trial
    """

    # Load the markers from the xdf file
    path = os.path.join(subject_path, 'EEG.xdf')
    data, header = pyxdf.load_xdf(path, [{'type': 'Markers'}])

    # Get the markers data and timestamps
    markers = [e[0] for e in data[0]['time_series']]
    markers_timestamps = data[0]['time_stamps']

    start = lsl_params['start_trial']
    trial_times = []

    for i in range(len(markers)):

        if markers[i] == start:
            trial_times.append((markers_timestamps[i], markers_timestamps[i + 1]))

    return trial_times


def MI_segment_data():

    # Get all the days folder for the current subject
    days = os.listdir(data_params['record_folder'])

    # For each subject segment the (clean) EEG data
    for day in days:

        day_path = os.path.join(data_params['record_folder'], day)

        # Load EEG data and markers data
        eeg_data = pd.read_csv(os.path.join(day_path, data_params['EEG_filename']))
        trial_times = get_trials_times(day_path)

        # Split the EEG data into trials according to markers
        eeg_trials = []

        for t in trial_times:
            start_time, stop_time = t
            trial = eeg_data[(start_time < eeg_data.time) & (eeg_data.time < stop_time)].reset_index(drop=True)

            # Drop weird trials
            if len(trial.index) >= 10:
                eeg_trials.append(trial.drop(['time'], axis=1))

        # Dump pickle file of the subject trials
        pickle.dump(eeg_trials, open(os.path.join(day_path, data_params['trials_filename']), 'wb'))


if __name__ == '__main__':

    MI_segment_data()