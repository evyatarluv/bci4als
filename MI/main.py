
"""
The main script which run all the MI steps
"""

from MI.MI1_record_experiment import MI_record
from MI.MI2_preprocess import MI_preprocess
from MI.MI3_segment_data import MI_segment_data
from MI.MI4_extract_features import MI_extract_features
<<<<<<< HEAD
# from MI.MI5_learn_model import MI5_learn_model
=======
from MI.MI5_learn_model import MI5_learn_model
>>>>>>> 895d0d0b933d59c8280f9813b5125f92a90e9652


if __name__ == '__main__':

<<<<<<< HEAD
    # MI_record()

    # MI_preprocess()

    MI_segment_data()
=======
    MI_record()

    # MI_preprocess()

    # MI_segment_data()
>>>>>>> 895d0d0b933d59c8280f9813b5125f92a90e9652

    # MI_extract_features(mode='cnn')

    # MI5_learn_model(r'C:\Users\noam\PycharmProjects\BCI-4-ALS2\data\evyatar', 'same day', 'svm')

