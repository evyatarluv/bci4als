import os
import pickle

import pandas as pd
import pyxdf

from config import params


def get_trials_times(subject_path):
    """
    This function get subject path and return a list of the trials timestamps.
    contains the trial start & end timestamps.
    :param subject_path: str, path to the current subject folder
    :return: list with tuples correspond to the start & end of each trial
    """

    # Load the markers from the xdf file
    path = os.path.join(subject_path, 'EEG.xdf')
    data, header = pyxdf.load_xdf(path, [{'type': 'Markers'}])

    # Get the markers data and timestamps
    markers = [e[0] for e in data[0]['time_series']]
    markers_timestamps = data[0]['time_stamps']

    start = params['lsl']['start_trial']
    trial_times = []

    for i in range(len(markers)):

        if markers[i] == start:
            trial_times.append((markers_timestamps[i], markers_timestamps[i + 1]))

    return trial_times


def MI_segment_data():
    # Debug
    print('---------- Start MI3 - Data Segmentation  ----------')

    # Get all the days folder for the current subject
    days = os.listdir(params['data']['subject_folder'])

    # For each subject segment the (clean) EEG data
    for day in days:

        day_path = os.path.join(params['data']['subject_folder'], day)

        # Load EEG data and markers data
        eeg_data = pd.read_csv(os.path.join(day_path, params['data']['filenames']['EEG_clean']))
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
        pickle.dump(eeg_trials, open(os.path.join(day_path, params['data']['filenames']['trials']), 'wb'))


if __name__ == '__main__':
    MI_segment_data()
