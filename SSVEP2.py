import mne
import pyxdf

"""
Preprocessing of EEG data
"""

data_path = 'EEG.xdf'

def main():

    # Load the EEG data
    eeg = pyxdf.load_xdf(data_path)

    print('h')

if __name__ == '__main__':

    main()