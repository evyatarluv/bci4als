from bci4als.ml_model import MLModel
from bci4als.experiments.online import OnlineExperiment
from bci4als.eeg import EEG


def run_experiment(model_path: str):

    model = MLModel(model_path=model_path)

    SYNTHETIC_BOARD = -1
    CYTON_DAISY = 2
    eeg = EEG(board_id=CYTON_DAISY)

    exp = OnlineExperiment(eeg=eeg, model=model, num_trials=10, buffer_time=4, threshold=3, skip_after=5)

    exp.run(use_eeg=True, full_screen=True)

    # exp.warmup(use_eeg=True, target='right')


if __name__ == '__main__':
    model_path = r'../recordings/avi/4/model.pickle'
    #model_path = None  # use if synthetic
    run_experiment(model_path=model_path)

# PAY ATTENTION!
# If synthetic - model Path should be none
# otherwise choose a model path
