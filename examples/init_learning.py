from bci4als.learning.experiment import Experiment


def main():

    exp = Experiment(num_trials=5, next_length=1, cue_length=0.25, ready_length=1, trial_length=3)

    eeg = exp.run()

    # eeg.preprocess()
    #
    # features = eeg.extract_features()
    #
    # model = train_model(features)


if __name__ == '__main__':

    main()
