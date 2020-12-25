
"""
The main script which runs the program
"""

from bci_4_als.bci_4_als.MI.record_experiment import MI_record
from bci_4_als.bci_4_als.MI.preprocess import MI_preprocess
from bci_4_als.bci_4_als.MI.segment_data import MI_segment_data
# from MI.MI4_extract_features import MI_extract_features
from bci_4_als.bci_4_als.MI.train_model import MI_train_model
from bci_4_als.bci_4_als.MI.test_model import MI_test

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
        MI_train_model('same day', 'svm')

    if test:
        MI_test()

