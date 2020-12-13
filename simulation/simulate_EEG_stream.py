"""
Example program to demonstrate how to send a multi-channel time series to LSL.
I used this example in order to simulate EEG stream
"""

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet


def main():

    # first create a new stream info (here we set the name to OpenBCI,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available
    info = StreamInfo('OpenBCI', 'EEG', 8, 100, 'float32', 'myuid34234')

    # next make an outlet
    outlet = StreamOutlet(info)

    input('Start recording via Lab Recorder and press enter...')
    print('Streaming EEG data...')

    while True:

        # Rand some EEG sample
        eeg_sample = [rand(), rand(), rand(), rand(), rand(), rand(), rand(), rand()]

        # Now send it and wait for a bit
        outlet.push_sample(eeg_sample)
        time.sleep(0.01)


if __name__ == '__main__':

    main()

