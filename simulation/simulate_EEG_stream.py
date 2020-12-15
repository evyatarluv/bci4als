"""
Example program to demonstrate how to send a multi-channel time series to LSL.
I used this example in order to simulate EEG stream
"""

import time
import numpy as np
from pylsl import StreamInfo, StreamOutlet

channels = 16
sample_rate = 120

def main():

    # Simulation of OpenBCI streaming using 16 channels and 120 Hz as sample rate
    info = StreamInfo('OpenBCI', 'EEG', channels, sample_rate, 'float32', 'myuid34234')
    outlet = StreamOutlet(info)

    input('Start recording via Lab Recorder and press enter...')
    print('Streaming EEG data...')

    while True:

        # Rand some EEG sample
        eeg_sample = np.random.rand(channels)

        # Now send it and wait for a bit
        outlet.push_sample(eeg_sample)
        time.sleep(1 / sample_rate)


if __name__ == '__main__':

    main()

