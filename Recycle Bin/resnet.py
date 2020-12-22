import os
import pickle
import cv2
import matplotlib.pyplot as plt
from keras.applications import resnet_v2


# Get all the subjects' folders
subjects = os.listdir('..\\data\\evyatar')

# For each subject extract features
for s in subjects:

    # Get the current subject trials
    subject_path = os.path.join('..\\data\\evyatar', s)
    trials_path = os.path.join(subject_path, 'EEG_trials.pickle')
    trials = pickle.load(open(trials_path, 'rb'))

    # for trial in trials:
    #
    #     resized_trial = cv2.resize(trial, (32, 500))
    #     plt.imshow(resized_trial)
    #     plt.show()
    #     input('IMAGE')
    #     resized_trial = cv2.merge((resized_trial, resized_trial, resized_trial))
    #     resnet = resnet_v2.ResNet50V2(include_top=False, weights='imagenet', input_shape=(500, 32))
    #     resnet.predict(trial)
