from bci4als.learning.offline import OfflineExperiment


def main():

    exp = OfflineExperiment(num_trials=5, trial_length=3)

    eeg = exp.run()

    # eeg.preprocess()
    #
    # features = eeg.extract_features()
    #
    # model = train_model(features)


if __name__ == '__main__':

    main()
