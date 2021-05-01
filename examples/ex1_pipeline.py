import os
import pickle

import mne.filter
import numpy as np
from mne_features.feature_extraction import extract_features
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score

base_path = "adi_eden_records"
filenames = ["Sub2011001.pkl", "Sub2111001.pkl", "Sub2211001.pkl"]
for fname in filenames:
    fpath = os.path.join(base_path, fname)
    files = pickle.load(open(fpath, 'rb'))

    data = files["data"]
    intervals = files["duration"]
    ch_names = files["ch_names"]
    labels = files["labels"]
    sfreq = 125  # todo: verify the sfreq used
    l_freq = 1
    h_freq = 30

    # transpose data
    data = data.T

    # convert to np.float64
    data = data.astype(np.float64)

    # bandpass filter
    data = mne.filter.filter_data(data, sfreq, l_freq, h_freq, verbose=False)

    # notch filter
    data = mne.filter.notch_filter(data, sfreq, 50, verbose=False)

    # select channels
    channels = ['C03', 'C04']
    data = data[[ch_names.index(channel) for channel in channels], :]

    # split to trials
    trials = [data[:, ival[0]:ival[1]] for ival in intervals]


    # trials = [mne.filter.notch_filter(trial, sfreq, 50) for trial in trials]

    # trim all trials to same length
    min_length = min([len(trial) for trial in trials])
    trials = [trial[:, :min_length] for trial in trials]

    # extract features
    selected_funcs = ['pow_freq_bands', 'mean', 'spect_edge_freq']
    mne_params = {
        # 'pow_freq_bands__freq_bands': np.arange(1, int(s_freq / 2), 1),
        'pow_freq_bands__freq_bands': {'band_1': [15.5, 18.5],
                                          'band_2': [8, 10.5],
                                          'band_3': [10, 15.5],
                                          # 'band_4': [17.5, 20.5],
                                          # 'band_5': [12.5, 30]
                                          }
    }
    X = np.stack(trials)
    features_df = extract_features(X, sfreq, selected_funcs, mne_params, return_as_df=True)
    features = features_df.values

    # train model on training set and evaluate with 5-fold cross validation
    clf = SGDClassifier()
    scores = cross_val_score(clf, features, labels, cv=5)
    print(f"scores for {fpath}: ", scores)
