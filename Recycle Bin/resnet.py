import os
import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.applications import resnet_v2
from sklearn.decomposition import PCA

image_size = (100, 600)

resnet = resnet_v2.ResNet50V2(include_top=False, weights='imagenet', pooling='avg',
                              input_shape=image_size[::-1] + (3,))
# Get the current subject trials
subject_path = os.path.join('..\\data\\evyatar', '1')
trials_path = os.path.join(subject_path, 'EEG_trials.pickle')
trials = pickle.load(open(trials_path, 'rb'))





# f = extract_features_resnet(trials, resnet)
