import numpy as np
from nptyping import ndarray
from typing import List, Tuple


class EEG:

    def __init__(self):

        # todo: what about the channels names? input argument?
        self.markers_row = 31  # Get it as arg
        self.labels: List[int] = []
        self.durations: List[Tuple] = []

        # Construct the labels & durations lists
        # self._extract_trials()

    def _extract_trials(self, data: ndarray):
        """
        The method get ndarray and extract the labels and durations from the data.
        :param data: the data from the board.
        :return:
        """

        # Get marker indices
        markers_idx = np.where(data[self.markers_row, :] != 0)[0]

        # For each marker
        for idx in markers_idx:

            # Decode the marker
            status, label, _ = self.decode_marker(data[self.markers_row, idx])

            if status == 'start':

                self.labels.append(label)
                self.durations.append((idx,))

            elif status == 'stop':

                self.durations[-1] = self.durations[-1] + (idx,)

    @staticmethod
    def encode_marker(status: str, label: int, index: int):
        """
        Encode a marker for the EEG data.
        :param status: status of the stim (start/end)
        :param label: the label of the stim (right -> 0, left -> 1, idle -> 2)
        :param index: index of the current label
        :return:
        """
        markerValue = 0
        if status == "start":
            markerValue += 1
        elif status == "stop":
            markerValue += 2
        else:
            raise ValueError("incorrect status value")

        markerValue += 10 * label

        markerValue += 100 * index

        return markerValue

    @staticmethod
    def decode_marker(marker_value: int):
        """
        Decode the marker and return a tuple with the status, label and index.
        Look for the encoder docs for explanation for each argument in the marker.
        :param marker_value:
        :return:
        """
        if marker_value % 10 == 1:
            status = "start"
            marker_value -= 1
        elif marker_value % 10 == 2:
            status = "stop"
            marker_value -= 2
        else:
            raise ValueError("incorrect status value")

        label = ((marker_value % 100) - (marker_value % 10)) / 10

        index = (marker_value - (marker_value % 100)) / 100

        return status, int(label), int(index)



