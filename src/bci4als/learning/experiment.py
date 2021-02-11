from brainflow import BrainFlowInputParams, BoardShim, BoardIds
from psychopy import event


class Experiment:

    def __init__(self, num_trials):

        self.num_trials = num_trials

    @staticmethod
    def _init_board(ip_port: int, serial_port: int) -> BoardShim:

        """
        Init board to have stream from.
        :param ip_port: ip port of the board
        :param serial_port: serial port of the board
        :return:
        """

        # Update the params
        params = BrainFlowInputParams()
        params.ip_port = ip_port
        params.serial_port = serial_port

        # Init board and prepare for session
        board = BoardShim(BoardIds.CYTON_DAISY_BOARD.value, params)
        board.prepare_session()

        return board

    @staticmethod
    def get_keypress():
        """
        Get keypress of the user
        :return: string of the key
        """

        keys = event.getKeys()
        if keys:
            return keys[0]
        else:
            return None

