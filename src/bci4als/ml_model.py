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

    def __init__(self, model_path: str = None):

        self.model_path = model_path
        self.model = pickle.load(open(model_path, 'rb')) if model_path is not None else None

    def offline_training(self, eeg: EEG, trials: List[pd.DataFrame], labels: List[int],
                         subject_folder: str, model_type: str):

        if model_type.lower() == 'csp_lda':

            self._csp_lda(eeg, trials, labels, subject_folder)

        else:

            raise NotImplementedError(f'The model type `{model_type}` is not implemented yet')

    def _csp_lda(self, eeg: EEG, trials: List[pd.DataFrame], labels: List[int], subject_folder: str):

        print('Training CSP & LDA model')

        # convert data to mne.Epochs
        ch_names = eeg.get_board_names()
        ch_types = ['eeg'] * len(ch_names)
        sfreq: int = eeg.sfreq
        n_samples: int = min([t.shape[0] for t in trials])
        epochs_array: np.ndarray = np.stack([df[:n_samples].to_numpy().T for df in trials])

        info = mne.create_info(ch_names, sfreq, ch_types)
        epochs = mne.EpochsArray(epochs_array, info)

        # set montage
        montage = make_standard_montage('standard_1020')
        epochs.set_montage(montage)

        # Apply band-pass filter
        epochs.filter(7., 30., fir_design='firwin', skip_by_annotation='edge')

        # Assemble a classifier
        lda = LinearDiscriminantAnalysis()
        csp = CSP(n_components=6, reg=None, log=True, norm_trace=False)

        # Use scikit-learn Pipeline
        clf = Pipeline([('CSP', csp), ('LDA', lda)])

        # fit transformer and classifier to data
        clf.fit(epochs.get_data(), labels)

        # save pipeline
        self.model_path = os.path.join(subject_folder, 'model.pickle')
        pickle.dump(clf, open(self.model_path, 'wb'))

        # save csp filters
        csp_figure_path = os.path.join(subject_folder, 'csp_filters.png')
        csp_plot_figure: Figure = csp.plot_patterns(epochs.info, ch_type='eeg', units='Patterns (AU)', size=1.5,
                                                    show=False)
        csp_plot_figure.savefig(csp_figure_path)

    def online_predict(self, data: NDArray, eeg: EEG):

        # Prepare the data to MNE functions
        data = data.astype(np.float64)

        # Filter the data (band-pass only)
        data = mne.filter.filter_data(data, l_freq=8, h_freq=30, sfreq=eeg.sfreq, verbose=False)

        # Predict
        prediction = self.model.predict(data[np.newaxis])[0]

        return prediction

