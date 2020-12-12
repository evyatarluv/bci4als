import os
import pyxdf
import numpy as np
import mne

data_params = {
    'sample_freq': None,
    'record_folder': 'C:\\Users\\lenovo\\Documents\\CurrentStudy',  # path to the folder with all the subjects
    'channel_names': ['C03', 'C04', 'P07', 'P08', 'O01', 'O02', 'F07', 'F08', 'F03', 'F04', 'T07', 'T08', 'P03'],
    'remove_channels': [0, 1, 2],  # channels to remove from the EEG data
}


filter_params = {
    'low_pass': 30,  # upper limit for low-pass filter
    'high_pass': 0.5,  # lower limit for high-pass filter
}


def load_eeg_data(folder_path):

    # Get the xdf file
    path = os.path.join(folder_path, 'EEG.xdf')
    data, header = pyxdf.load_xdf(path, [{'type': 'EEG'}])

    # Get the EEG data & update sample rate param
    eeg_data = data[0]['time_series']
    data_params['sample_freq'] = int(data[0]['info']['nominal_srate'][0])  # update the sample rate

    # Remove channels
    eeg_data = np.delete(eeg_data, obj=data_params['remove_channels'], axis=1)

    # Debug print
    print('EEG data loaded\nData shape: {}'.format(eeg_data.shape))

    return eeg_data


def filter_eeg_data(eeg):

    """
    Filter the raw EEG data.
    All the filtering part will be in this function
    :param eeg: ndarray, the raw EEG data of subject (channels as columns)
    :return: ndarray, the filtered EEG data (channels as columns)
    """

    # Params
    low_pass = filter_params['low_pass']
    high_pass = filter_params['high_pass']
    sample_freq = data_params['sample_freq']

    # Convert to float64 in order to fit mne functions
    eeg = eeg.astype(np.float64)
    eeg = eeg.T  # mne functions look for the channels as rows

    # Low-pass filter
    eeg = mne.filter.filter_data(eeg, l_freq=None, h_freq=low_pass, sfreq=sample_freq)

    # High-pass filter
    eeg = mne.filter.filter_data(eeg, l_freq=high_pass, h_freq=None, sfreq=sample_freq)

    return eeg.T


def MI_preprocess():
    # Get all the subjects' folders
    subjects = os.listdir(data_params['record_folder'])

    # For each subject clean the EEG data
    for s in subjects:

        eeg_data = load_eeg_data(os.path.join(data_params['record_folder'], s))

        eeg_data = filter_eeg_data(eeg_data)

        save_clean_eeg(eeg_data)


if __name__ == '__main__':
    MI_preprocess()
