from typing import List

from mne.io import RawArray
import mne
import pandas as pd
from bci4als.learning.eeg import EEG
from bci4als.learning.offline import OfflineExperiment


def preprocess(eeg: EEG, trials: List[pd.DataFrame]) -> List[RawArray]:

    filtered_trials = []

    for trial in trials:

        # Create MNE RawArray object
        eeg_data = trial.to_numpy() / 1000000  # BrainFlow returns uV, convert to V for MNE
        ch_types = ['eeg'] * len(eeg_data)
        info = mne.create_info(ch_names=eeg.eeg_names, sfreq=eeg.sfreq, ch_types=ch_types)
        raw = RawArray(eeg_data, info)

        # Filter the data
        raw = EEG.filter_data(raw, notch=50, low_pass=4, high_pass=48)

        # Append to the filtered list
        filtered_trials.append(raw)

    return filtered_trials


def main():

    eeg = EEG(board_id=2, ip_port=6677, serial_port="COM4")

    exp = OfflineExperiment(eeg=eeg, num_trials=5, trial_length=3)

    trials, labels = exp.run()

    trials = preprocess(eeg, trials)

    # features = eeg.extract_features()
    #
    # model = train_model(features)


if __name__ == '__main__':

    main()
