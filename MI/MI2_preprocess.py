"""
This script filter EEG raw data.

The main function need to have a recording folder - the folder where all the subjects' folder locate.
Then it run over each subject and:
    1. Load the EEG data as ndarray
    2. Filter the raw data
    3. Save the cleaned data in the subject's folder.
"""
import json
import os
import pyxdf
import numpy as np
import mne
import pandas as pd
import yaml

# Configurations
config = yaml.full_load(open('config.yaml', 'r'))
data_params = config['data']
preprocess_params = config['preprocess']


def load_eeg_data(folder_path):

    """
    Load the raw EEG data from the xdf file.
    :param folder_path: path to the folder where the xdf file was located
    :return: ndarray, EEG data
    """

    # Get the xdf file
    path = os.path.join(folder_path, 'EEG.xdf')
    data, header = pyxdf.load_xdf(path, [{'type': 'EEG'}])

    # Get the EEG data & update sample rate param
    eeg_data = data[0]['time_series']
    eeg_timestamp = data[0]['time_stamps']
    data_params['sample_freq'] = float(data[0]['info']['effective_srate'])  # update the sample rate

    # Remove channels
    eeg_data = np.delete(eeg_data, obj=preprocess_params['remove_channels'], axis=1)

    # Debug print
    print('EEG data loaded\nData shape: {}'.format(eeg_data.shape))

    # Dump the info as JSON
    json.dump(data[0]['info'], open(os.path.join(folder_path, '.info'), 'w'))

    return eeg_data, eeg_timestamp


def filter_eeg_data(eeg):

    """
    Filter the raw EEG data.
    All the filtering part will be in this function
    :param eeg: ndarray, the raw EEG data of subject (channels as columns)
    :return: ndarray, the filtered EEG data (channels as columns)
    """

    # Params
    low_pass = preprocess_params['filter']['low_pass']
    high_pass = preprocess_params['filter']['high_pass']
    sample_freq = data_params['sample_freq']

    # Convert to float64 in order to fit mne functions
    eeg = eeg.astype(np.float64)
    eeg = eeg.T  # mne functions look for the channels as rows

    # Lie about the sample rate
    if sample_freq < 100:
        sample_freq = 125

    # Low-pass filter
    eeg = mne.filter.filter_data(eeg, l_freq=None, h_freq=low_pass, sfreq=sample_freq)

    # High-pass filter
    eeg = mne.filter.filter_data(eeg, l_freq=high_pass, h_freq=None, sfreq=sample_freq)

    return eeg.T


def save_clean_eeg(eeg, time_stamps, subject_path):

    """
    This function export the cleaned EEG data.
    The function add the channels' names and then save it as csv file with '_clean' ending.
    :param time_stamps:
    :param eeg: ndarray of the cleaned EEG data
    :param subject_path: the path to the current subject's folder
    :return:
    """

    # Add channel names
    eeg = np.c_[time_stamps, eeg]
    cleaned_eeg = pd.DataFrame(data=eeg, columns=preprocess_params['channel_names'])

    # Output the cleaned EEG
    output_path = os.path.join(subject_path, data_params['filenames']['EEG_clean'])
    cleaned_eeg.to_csv(output_path, index=False)


def MI_preprocess():

    print('---------- Start MI2 - Data Pre-Processing  ----------')

    # Get all the days in the subject folder
    days = os.listdir(data_params['subject_folder'])

    # For each subject clean the EEG data
    for day in days:

        day_path = os.path.join(data_params['subject_folder'], day)

        eeg_data, eeg_timestamp = load_eeg_data(day_path)

        eeg_data = filter_eeg_data(eeg_data)

        save_clean_eeg(eeg_data, eeg_timestamp, day_path)


if __name__ == '__main__':

    MI_preprocess()
