import numpy as np
import pandas as pd
from brainflow import BrainFlowInputParams, BoardShim, BoardIds


class EEG:
    def __init__(self, board_id=BoardIds.CYTON_DAISY_BOARD.value, ip_port=6677, serial_port="COM3"):
        self.board_id = board_id
        self.params = BrainFlowInputParams()
        self.params.ip_port = ip_port
        self.params.serial_port = serial_port
        self.board = BoardShim(board_id, self.params)
        self.sfreq = self.board.get_sampling_rate(board_id)

        self.buffer = None

        # self.labels: List[int] = []
        # self.durations: List[Tuple] = []

        # Construct the labels & durations lists
        # self._extract_trials()

    # def _extract_trials(self, data: NDArray):
    #     """
    #     The method get ndarray and extract the labels and durations from the data.
    #     :param data: the data from the board.
    #     :return:
    #     """
    #
    #     # Get marker indices
    #     markers_idx = np.where(data[self.markers_row, :] != 0)[0]
    #
    #     # For each marker
    #     for idx in markers_idx:
    #
    #         # Decode the marker
    #         status, label, _ = self.decode_marker(data[self.markers_row, idx])
    #
    #         if status == 'start':
    #
    #             self.labels.append(label)
    #             self.durations.append((idx,))
    #
    #         elif status == 'stop':
    #
    #             self.durations[-1] = self.durations[-1] + (idx,)

    def on(self):
        """Turn EEG On"""
        self.board.prepare_session()
        self.board.start_stream()

    def off(self):
        """Turn EEG Off"""
        self.board.stop_stream()
        self.board.release_session()

    def insert_marker(self, status: str, label: int, index: int):
        """Insert an encoded marker into EEG data"""
        marker = self.encode_marker(status, label, index)
        self.board.insert_marker(marker)

    def _numpy_to_df(self, board_data):
        # create dictionary of <col index,col name>
        eeg_channels = self.board.get_eeg_channels(self.board_id)
        eeg_names = self.board.get_eeg_names(self.board_id)
        timestamp_channel = self.board.get_timestamp_channel(self.board_id)
        acceleration_channels = self.board.get_accel_channels(self.board_id)
        marker_channel = self.board.get_marker_channel(self.board_id)

        column_names = {}
        column_names.update(zip(eeg_channels, eeg_names))
        column_names.update(zip(acceleration_channels, ['X', 'Y', 'Z']))
        column_names.update({timestamp_channel: "timestamp",
                             marker_channel: "marker"})

        df = pd.DataFrame(board_data.T)
        df.rename(columns=column_names)

        # drop unused channels
        df = df[column_names]

        # decode int markers
        df['marker'] = df['marker'].apply(self.decode_marker)
        df[['marker_status', 'marker_label', 'marker_index']] = pd.DataFrame(df['marker'].tolist(), index=df.index)
        return df

    def _preprocess(self, board_data):
        # todo: signal processing (Notch Filter @ 50Hz, Bandpass Filter, Artifact Removal)
        raise NotImplementedError

    def get_raw_data(self):
        """
        The method returns dataframe with all the raw data, and empties the buffer

        :param:
        :return:
        """
        data = self.board.get_board_data()
        df = self._numpy_to_df(data)
        return df

    def get_processed_data(self):
        """
        The method returns dataframe with all the preprocessed (filters etc.) data, and empties the buffer

        :param:
        :return:
        """
        # todo: implement this
        raise NotImplementedError

    def get_features(self):
        # todo: implement this
        raise NotImplementedError


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
