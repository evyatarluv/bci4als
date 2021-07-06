import os
import pickle
from bci4als.eeg import EEG
from bci4als.ml_model import MLModel
from bci4als.experiments.offline import OfflineExperiment


def offline_experiment():

    SYNTHETIC_BOARD = -1
    CYTON_DAISY = 2
    eeg = EEG(board_id=CYTON_DAISY)

    exp = OfflineExperiment(eeg=eeg, num_trials=20, trial_length=5,
                            full_screen=True, audio=False)

    trials, labels = exp.run()

    # Classification
    model = MLModel(trials=trials, labels=labels)
    session_directory = exp.session_directory
    model.offline_training(eeg=eeg, model_type='csp_lda')

    # Dump the MLModel
    pickle.dump(model, open(os.path.join(session_directory, 'model.pickle'), 'wb'))


if __name__ == '__main__':

    offline_experiment()

