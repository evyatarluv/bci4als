
"""
The main script which run all the MI steps
"""

from MI.MI1_record_experiment import MI_record
from MI.MI2_preprocess import MI_preprocess
from MI.MI3_segment_data import MI_segment_data
from MI.MI4_extract_features import MI_extract_features
from MI.MI5_learn_model import MI5_learn_model


if __name__ == '__main__':

    # MI_record()

    MI_preprocess()

    # MI_segment_data()

    # MI_extract_features()

    # MI5_learn_model('..\\data\\evyatar', 'same day', 'svm')

