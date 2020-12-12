
import os

data_params = {
    'record_folder': 'C:/Users/lenovo/Documents/CurrentStudy'
}


def MI_preprocess():

    # Get all the subjects' folders
    subjects = os.listdir(data_params['record_folder'])

    # For each subject clean the EEG data
    for s in subjects:

        eeg_data = load_eeg_data()

        eeg_data = filter_eeg_data(eeg_data)

        save_clean_eeg(eeg_data)


if __name__ == '__main__':

    MI_preprocess()