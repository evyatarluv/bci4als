from bci4als.learning.eeg import EEG
from bci4als.learning.offline import OfflineExperiment


def main():

    eeg = EEG(board_id=2, ip_port=6677, serial_port="COM4")

    exp = OfflineExperiment(eeg=eeg, num_trials=5, trial_length=3)

    eeg = exp.run()

    # eeg.preprocess()
    #
    # features = eeg.extract_features()
    #
    # model = train_model(features)


if __name__ == '__main__':

    main()
