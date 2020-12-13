import time
from random import random as rand
import pylsl


def main():

    info = pylsl.StreamInfo('MarkerStream', 'Markers', 1, 0, 'string', 'myuniquesourceid23443')
    outlet_stream = pylsl.StreamOutlet(info)

    input('Start recording via Lab Recorder and press enter...')

    while True:

        # Push start trial
        input('Press to push `Start` sample')
        outlet_stream.push_sample('1')

        # Push start trial
        input('Press to push `End` sample')
        outlet_stream.push_sample('11')


if __name__ == '__main__':

    main()

