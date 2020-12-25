
"""
The main script which runs all the MI steps
"""

# from MI.MI1_record_experiment import MI_record
from MI.MI1_record_experiment import MI_record
from MI.MI2_preprocess import MI_preprocess
from MI.MI3_segment_data import MI_segment_data
# from MI.MI4_extract_features import MI_extract_features
from MI.MI5_train import MI5_learn_model


if __name__ == '__main__':

    record = False
    preprocess = False
    segment = False
    train = False
    test = False

    # Begin an experiment recording.
    # Streams raw EEG data
    if record:
        MI_record()

    # Apply filters and artifact removal
    if preprocess:
        MI_preprocess()

    # Segment into annotated trials
    if segment:
        MI_segment_data()


    # MI_extract_features()
    if train:
        MI5_learn_model('same day', 'svm')

    if test:
        MI6_test()

