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

filter_params = {
    'low_pass': 40,
    'high_pass': 0.5,
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

    # Get the EEG data
    eeg_data = data[eeg_index]['time_series']

    # Update channels name
    # TODO: Update this according to OpenBCI setup
    # eeg_data = np.delete(eeg_data, obj=0, axis=1)  # Delete the first channel
    # eeg_data = pd.DataFrame(data=eeg_data, columns=data_params['channel_names'])  # Add channels names

    # Debug print
    print('EEG data loaded\nData shape: {}'.format(eeg_data.shape))
    return eeg_data


def filter_eeg_data(eeg):

    """
    All the filtering part will be in this function
    :param eeg: ndarray of the original EEG data
    :return: ndarray of the filtered EEG data
    """

    # Low-pass filter
    eeg = mne.filter.filter_data(eeg, h_freq=40)

    # High-pass filter
    eeg = mne.filter.filter_data(eeg, l_freq=0.5)

def main():

    # Load the EEG data
    eeg = get_eeg_data()

    # Filter the data
    eeg = filter_eeg_data(eeg)



if __name__ == '__main__':

    main()