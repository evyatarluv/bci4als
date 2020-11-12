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
    labels_index = data_params['labels_index']


    # TODO: get params from the function
    data, header = pyxdf.load_xdf(path)

    # Get the EEG data
    channel_count = int(data[eeg_index]['info']['channel_count'][0])
    eeg = pd.DataFrame(data=data[eeg_index]['time_series'],
                       columns=list(range(1, channel_count + 1)))
    eeg['time'] = data[eeg_index]['time_stamps']

    print('g')


def main():

    # Load the EEG data
    eeg = get_eeg_data()

    print('h')


if __name__ == '__main__':

    main()