import os
import numpy as np
import pandas as pd

data_params = {
    'record_folder': 'C:\\Users\\lenovo\\Documents\\CurrentStudy',  # path to the folder with all the subjects
}


def load_eeg_data(subject_path):




def MI_segment_data():

    # Get all the subjects' folders
    subjects = os.listdir(data_params['record_folder'])

    # For each subject clean the EEG data
    for s in subjects:

        subject_path = os.path.join(data_params['record_folder'], s)

        eeg_data = load_eeg_data(subject_path)

        eeg_data = filter_eeg_data(eeg_data)

        save_clean_eeg(eeg_data, subject_path)

if __name__ == '__main__':

    MI_segment_data()