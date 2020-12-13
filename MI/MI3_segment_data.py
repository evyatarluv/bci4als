import os
import numpy as np
import pandas as pd
import pyxdf
from MI.MI1_training import lsl_params
import pickle

data_params = {
    'record_folder': 'C:\\Users\\lenovo\\Documents\\CurrentStudy',  # path to the folder with all the subjects
    'EEG_filename': 'EEG_clean.csv',
}


def load_markers(subject_path):

    # Load the markers from the xdf file
    path = os.path.join(subject_path, 'EEG.xdf')
    data, header = pyxdf.load_xdf(path, [{'type': 'Markers'}])

    # Get the markers data and timestamps
    markers = [e[0] for e in data[0]['time_series']]
    markers_timestamps = data[0]['time_stamps']

    start = lsl_params['start_trial']
    end = lsl_params['end_trial']
    trial_times = []

    for i in range(len(markers)):
        if markers[i] == start:
            trial_times.append((markers_timestamps[i], markers_timestamps[i + 1]))

    return trial_times


def MI_segment_data():

    # Get all the subjects' folders
    subjects = os.listdir(data_params['record_folder'])

    # For each subject clean the EEG data
    for s in subjects:

        subject_path = os.path.join(data_params['record_folder'], s)

        # Load EEG data and markers data
        eeg_data = pd.read_csv(os.path.join(subject_path, data_params['EEG_filename']))
        trial_times = load_markers(subject_path)

        # Split the EEG data into trials according to markers
        eeg_trials = []

        for t in trial_times:
            start_time, stop_time = t
            trial = eeg_data[(start_time < eeg_data.time) & (eeg_data.time < stop_time)]
            eeg_trials.append(trial.drop(['time']))

        # Dump pickle file of the subject trials
        pickle.dump(eeg_trials, open(os.path.join(subject_path, 'EEG_trials.pickle'), 'wb'))


if __name__ == '__main__':

    MI_segment_data()