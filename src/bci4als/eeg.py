from typing import List, Tuple

import mne
import numpy as np
import pandas as pd
from brainflow import BrainFlowInputParams, BoardShim, BoardIds
from mne_features.feature_extraction import extract_features
from nptyping import NDArray


class EEG:

    def __init__(self, board_id=BoardIds.CYTON_DAISY_BOARD.value, ip_port=6677, serial_port="COM3"):

        # Board params
        self.board_id = board_id
        self.params = BrainFlowInputParams()
        self.params.ip_port = ip_port
        self.params.serial_port = serial_port
        self.board = BoardShim(board_id, self.params)
        self.sfreq = self.board.get_sampling_rate(board_id)
        self.marker_row = self.board.get_marker_channel(self.board_id)
        self.eeg_names = self.board.get_eeg_names(board_id)

        # Features params
        # todo: get as arg
        self.features_params = {'channels': ['C03', 'C04']}

    def extract_trials(self, data: NDArray) -> [List[Tuple], List[int]]:
        """
        The method get ndarray and extract the labels and durations from the data.
        :param data: the data from the board.
        :return:
        """

        # Init params
        durations, labels = [], []

        # Get marker indices
        markers_idx = np.where(data[self.marker_row, :] != 0)[0]

        # For each marker
        for idx in markers_idx:

            # Decode the marker
            status, label, _ = self.decode_marker(data[self.marker_row, idx])

            if status == 'start':

                labels.append(label)
                durations.append((idx,))

            elif status == 'stop':

                durations[-1] += (idx,)

        return durations, labels

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

        marker = self.encode_marker(status, label, index)  # encode marker
        self.board.insert_marker(marker)  # insert the marker to the stream

        # print(f'Status: { status }, Marker: { marker }')  # debug
        # print(f'Count: { self.board.get_board_data_count() }')  # debug

    def _numpy_to_df(self, board_data: NDArray):
        """
        gets a Brainflow-style matrix and returns a Pandas Dataframe
        :param board_data: NDAarray retrieved from the board
        :returns df: a dataframe with the data
        """
        # create dictionary of <col index,col name> for renaming DF
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

    def _board_to_mne(self, board_data: NDArray, ch_names: List[str]) -> mne.io.RawArray:
        """
        Convert the ndarray board data to mne object
        :param board_data: raw ndarray from board
        :return:
        """
        eeg_data = board_data / 1000000  # BrainFlow returns uV, convert to V for MNE

        # Creating MNE objects from BrainFlow data arrays
        ch_types = ['eeg'] * len(board_data)
        info = mne.create_info(ch_names=ch_names, sfreq=self.sfreq, ch_types=ch_types)
        raw = mne.io.RawArray(eeg_data, info, verbose=False)

        return raw

    def get_raw_data(self, ch_names: List[str]) -> mne.io.RawArray:
        """
        The method returns dataframe with all the raw data, and empties the buffer

        :param ch_names: list[str] of channels to select
        :return: mne_raw data
        """

        indices = [self.eeg_names.index(ch) for ch in ch_names]

        data = self.board.get_board_data()[indices]

        return self._board_to_mne(data, ch_names)

    def get_features(self, channels: List[str], selected_funcs: List[str],
                     notch: float = 50, low_pass: float = 4, high_pass: float = 50) -> NDArray:
        """
        Returns features of all data since last call to get_board_data method.
        :return features: NDArray of shape (1, n_features)
        """

        # Get the raw data
        data = self.get_raw_data(ch_names=channels)

        # Filter
        data = self.filter_data(data, notch, low_pass, high_pass)

        # Extract features
        features = extract_features(data.get_data()[np.newaxis], self.sfreq,
                                    selected_funcs,
                                    {'pow_freq_bands__freq_bands': np.array([8, 10, 12.5, 30])})

        return features

    def clear_board(self):
        """Clear all data from the EEG board"""

        # Get the data and don't save it
        self.board.get_board_data()

    def get_board_data(self) -> NDArray:
        """The method returns the data from board and remove it"""
        return self.board.get_board_data()

    def get_board_names(self, alternative=True) -> List[str]:
        """The method returns the board's channels"""
        if alternative:
            # return ['Fp1', 'Fp2', 'C3', 'C4', 'CP5', 'CP6', 'O1', 'O2', 'FC1', 'FC2', 'Cz', 'T8', 'FC5', 'FC6', 'CP1', 'CP2']
            return ['CP2', 'FC2', 'CP6', 'C4', 'C3', 'CP5', 'FC1', 'CP1', 'Cz', 'FC6', 'T8', 'T7', 'FC5']
        else:
            return self.board.get_eeg_names(self.board_id)

    def get_board_channels(self, alternative=True) -> List[int]:
        """Get list with the channels locations as list of int"""
        if alternative:
            return self.board.get_eeg_channels(self.board_id)[:-3]
        else:
            return self.board.get_eeg_channels(self.board_id)

    def get_channels_data(self):
        """Get NDArray only with the channels data (without all the markers and other stuff)"""
        return self.board.get_board_data()[self.board.get_eeg_channels(self.board_id)]

    @staticmethod
    def filter_data(data: mne.io.RawArray,
                    notch: float, low_pass: float, high_pass: float) -> mne.io.RawArray:

        # data.notch_filter(freqs=notch, verbose=False)
        data.filter(l_freq=low_pass, h_freq=high_pass, verbose=False)

        return data

    @staticmethod
    def encode_marker(status: str, label: int, index: int):
        """
        Encode a marker for the EEG data.
        :param status: status of the stim (start/end)
        :param label: the label of the stim (right -> 0, left -> 1, idle -> 2, tongue -> 3, legs -> 4)
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
    def decode_marker(marker_value: int) -> (str, int, int):
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
            raise ValueError("incorrect status value. Use start or stop.")

        label = ((marker_value % 100) - (marker_value % 10)) / 10

        index = (marker_value - (marker_value % 100)) / 100

        return status, int(label), int(index)

    @staticmethod
    def laplacian(data: NDArray, channels: List[str]):
        """
        The method execute laplacian on the raw data.
        The laplacian was computed as follows:
            1. C3 = C3 - mean(Cz + F3 + P3 + T3)
            2. C4 = C4 - mean(Cz + F4 + P4 + T4)

        The data need to be (n_channel, n_samples)
        :return:
        """

        # Dict with all the indices of the channels
        idx = {ch: channels.index(ch) for ch in channels}

        # C3
        data[idx['C3']] -= (data[idx['Cz']] + data[idx['FC5']] + data[idx['FC1']] +
                            data[idx['CP5']] + data[idx['CP1']]) / 5

        # C4
        data[idx['C4']] -= (data[idx['Cz']] + data[idx['FC2']] + data[idx['FC6']] +
                            data[idx['CP2']] + data[idx['CP6']]) / 5

        return data[[idx['C3'], idx['C4']]]
