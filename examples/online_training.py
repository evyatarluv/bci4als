from bci4als.ml_model import MLModel
from bci4als.experiments.online import OnlineExperiment
from bci4als.eeg import EEG


def run_experiment(model_path: str):

    model = MLModel(model_path=model_path)

    SYNTHETIC_BOARD = -1
    CYTON_DAISY = 2
    eeg = EEG(board_id=SYNTHETIC_BOARD)

    exp = OnlineExperiment(eeg=eeg, model=model, num_trials=3, buffer_time=4, threshold=3, skip_after=10)

    exp.run(use_eeg=True, full_screen=True)

    # exp.warmup(use_eeg=True, target='right')


if __name__ == '__main__':

    run_experiment(model_path=r'C:\Users\noam\PycharmProjects\bci_4_als\recordings\noam\1\model.pickle')
