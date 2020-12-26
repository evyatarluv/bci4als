import mne
import mne_features
import numpy as np
from mne_features.feature_extraction import extract_features

from moabb.datasets import physionet_mi

if __name__ == '__main__':
    # get dataset
    ds = physionet_mi.PhysionetMI()
    raw = ds.get_data([2])[2]['session_0']['run_4'].pick_channels(['C3', 'C4'])
    events = mne.events_from_annotations(raw)
    s_freq = raw.info['sfreq']

    # get x and save to file
    X = mne.Epochs(raw, events[0]).get_data()

    # extract features
    extract_features()
    params = {
        'pow_freq_bands__freq_bands': np.arange(1, int(s_freq / 2), 1),
    }
    selected_funcs = {'mean', 'ptp_amp', 'std', 'pow_freq_bands'}
    features_array = mne_features.feature_extraction.extract_features(X, s_freq, selected_funcs, params)

    # save features to file
    np.savetxt('../data/mne/1/features.csv', features_array, delimiter=',')

    # get y and save to file
    y = np.asarray([e[2] for e in events[0]])
    np.savetxt('../data/mne/1/stimulus_vectors.csv', y)
