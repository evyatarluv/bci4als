import mne
import pyxdf
import pandas as pd
import numpy as np

"""
Preprocessing of EEG data
"""

data_params = {
    'path': 'exp_example.xdf',
    'eeg_index': 1,
    'labels_index': 0,
}


def get_eeg_data():

    """

    :return:
    """

    # Get the params
    path = data_params['path']
    eeg_index = data_params['eeg_index']

    # Get the xdf file
    data, header = pyxdf.load_xdf(path)

    # Return the EEG data
    return data[eeg_index]['time_series']


def main():

    # Load the EEG data
    eeg = get_eeg_data()
    print('Loaded EEG data\nEEG data shape: {}'.format(eeg.shape))


if __name__ == '__main__':

    main()