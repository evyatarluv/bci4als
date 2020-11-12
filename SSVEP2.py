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
    'channel_names': ['Fp1', 'Fp2', 'C03', 'C04', 'P07', 'P08', 'O01', 'O02',
                      'F07', 'F08', 'F03', 'F04', 'T07', 'T08', 'P03']
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

    # Get the EEG data & add channel names
    eeg_data = data[eeg_index]['time_series']
    eeg_data = pd.DataFrame(data=eeg_data, columns=data_params['channel_names'])

    # Debug print
    print('EEG data loaded\nData shape: {}'.format(eeg_data.shape))
    return eeg_data


def main():

    # Load the EEG data
    eeg = get_eeg_data()



if __name__ == '__main__':

    main()