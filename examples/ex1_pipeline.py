import numpy as np
import pickle
import pyxdf
from mne_features.feature_extraction import extract_features

fpath = "adi_eden_records/Sub2011001.pkl"

files = pickle.load(open(fpath, 'rb'))

data = files["data"]
intervals = files["duration"]
ch_names = files["ch_names"]
labels = files["labels"]
sfreq = 120 #todo: verify the sfreq used

# select channels
channels = ['C03', 'C04']
data = data[:, [ch_names.index(channel) for channel in channels]]

# Step - Split to Trials
trials = [data[ival[0]:ival[1], :] for ival in intervals]

# Step - Extract Features

# trim all trials to same length
min_length = min([len(trial) for trial in trials])
trials = [trial[:min_length] for trial in trials]

# convert trials to np.float64
trials = [trial.astype(np.float64) for trial in trials]

# transpose trials
trials = [trial.T for trial in trials]

selected_funcs = ['energy_freq_bands']
mne_params = {
    # 'pow_freq_bands__freq_bands': np.arange(1, int(s_freq / 2), 1),
    'energy_freq_bands__freq_bands': {'low_alpha': [8, 10],
                                      'high_alpha': [10, 12.5],
                                      'beta': [12.5, 29]}
}
X = np.stack(trials)
features = extract_features(X, sfreq, selected_funcs, mne_params, return_as_df=False)
# Step - Split to Train, Validation, Test sets


# Step - Train Model on Training Set

# Step - Tune hyperparameters on validation set

# Step - Evaluate on test set
