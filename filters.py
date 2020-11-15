"""
Python low-pass and high-pass filters
"""

import numpy as np
from scipy.signal import butter, filtfilt


def butter_lowpass_filter(data, cutoff, fs, order=5):
    """

    :param data: data to filter
    :param cutoff: desired cutoff frequency of the filter, Hz
    :param fs: sample rate, Hz
    :param order:
    :return:
    """

    nyq = 0.5 * fs  # Nyquist Frequency

    normal_cutoff = cutoff / nyq

    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)

    return y

