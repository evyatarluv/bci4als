"""
Python low-pass and high-pass filters
"""

import numpy as np
from scipy.signal import butter, lfilter, freqz
from matplotlib import pyplot as plt


def butter_lowpass(cutoff, fs, order=5):

    """

    :param cutoff: desired cutoff frequency of the filter, Hz
    :param fs: sample rate, Hz
    :param order:
    :return:
    """

    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def plot_freqz(b, a, cutoff, fs):

    # Plot the frequency response.
    w, h = freqz(b, a, worN=8000)
    plt.subplot(2, 1, 1)
    plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
    plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
    plt.axvline(cutoff, color='k')
    plt.xlim(0, 0.5 * fs)
    plt.title("Lowpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid()


def butter_lowpass_filter(data, cutoff, fs, order=5):

    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)

    plot_freqz(b, a, cutoff, fs)

    return y

