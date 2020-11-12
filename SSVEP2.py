import mne
import pyxdf

"""
Preprocessing of EEG data
"""

data_params = {
    'path': 'EEG.xdf',
    'eeg_index': 1,
    'labels_index': 0,
}


def get_eeg_data():
    """

    :return:
    """

    # TODO: get params from the function
    data, header = pyxdf.load_xdf('exp_example.xdf')

    # Get the EEG data
    data[1]


def main():

    # Load the EEG data
    eeg = get_eeg_data()

    print('h')


if __name__ == '__main__':

    main()