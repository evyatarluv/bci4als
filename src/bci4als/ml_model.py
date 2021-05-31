import os
import pickle
from typing import List
import mne
import pandas as pd
from bci4als.eeg import EEG
import numpy as np
from matplotlib.figure import Figure
from mne.channels import make_standard_montage
from mne.decoding import CSP
from nptyping import NDArray
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import Pipeline


class MLModel:

    def __init__(self, trials: List[pd.DataFrame], labels: List[int]):

        self.trials: List[NDArray] = [t.to_numpy().T for t in trials]
        self.labels: List[int] = labels
        self.debug = True
        self.clf = None

    def offline_training(self, eeg: EEG, model_type: str):

        if model_type.lower() == 'csp_lda':

            self._csp_lda(eeg)

        else:

            raise NotImplementedError(f'The model type `{model_type}` is not implemented yet')

    def _csp_lda(self, eeg: EEG):

        print('Training CSP & LDA model')

        # convert data to mne.Epochs
        ch_names = eeg.get_board_names()
        ch_types = ['eeg'] * len(ch_names)
        sfreq: int = eeg.sfreq
        n_samples: int = min([t.shape[1] for t in self.trials])
        epochs_array: np.ndarray = np.stack([t[:, :n_samples] for t in self.trials])

        info = mne.create_info(ch_names, sfreq, ch_types)
        epochs = mne.EpochsArray(epochs_array, info)

        # set montage
        montage = make_standard_montage('standard_1020')
        epochs.set_montage(montage)

        # Apply band-pass filter
        epochs.filter(7., 30., fir_design='firwin', skip_by_annotation='edge', verbose=False)

        # Assemble a classifier
        lda = LinearDiscriminantAnalysis()
        csp = CSP(n_components=6, reg=None, log=True, norm_trace=False)

        # Use scikit-learn Pipeline
        self.clf = Pipeline([('CSP', csp), ('LDA', lda)])

        # fit transformer and classifier to data
        self.clf.fit(epochs.get_data(), self.labels)

    def online_predict(self, data: NDArray, eeg: EEG):
        # Prepare the data to MNE functions
        data = data.astype(np.float64)

        # Filter the data ( band-pass only)
        data = mne.filter.filter_data(data, l_freq=8, h_freq=30, sfreq=eeg.sfreq, verbose=False)

        # Predict
        prediction = self.clf.predict(data[np.newaxis])[0]

        return prediction

    def partial_fit(self, eeg, X: NDArray, y: int):

        # Append X to trials
        self.trials.append(X)

        # Append y to labels
        self.labels.append(y)

        # Fit with trials and labels
        self._csp_lda(eeg)

