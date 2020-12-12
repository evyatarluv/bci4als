
import os
import pyxdf
import numpy as np

data_params = {
    'record_folder': 'C:\\Users\\lenovo\\Documents\\CurrentStudy'  # path to the folder with all the subjects
}


def load_eeg_data(folder_path):

    # Create the data path
    path = os.path.join(folder_path, 'EEG.xdf')

    # Get the xdf file
    data, header = pyxdf.load_xdf(path, [{'type': 'EEG'}])

    # Get the EEG data
    eeg_data = data[0]['time_series']

    # Remove the first channel
    eeg_data = np.delete(eeg_data, obj=0, axis=1)

    # Debug print
    print('EEG data loaded\nData shape: {}'.format(eeg_data.shape))

    return eeg_data



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