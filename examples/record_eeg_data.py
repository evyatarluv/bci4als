from bci4als.eeg import EEG
from brainflow import BoardIds


# initialize parameters
num_trials = 4

# board_id = BoardIds.CYTON_DAISY_BOARD  # The real deal
board_id = BoardIds.SYNTHETIC_BOARD  # Only for prototyping
eeg = EEG(board_id=board_id, ip_port=6677, serial_port="COM6")

# Start stream
eeg.on()

#
# # Run trials
# for i in range(num_trials):
#     # Messages for user
#     self._user_messages(i)
#
#     # Show the stimulus
#     self.eeg.insert_marker(status='start', label=self.labels[i], index=i)
#     self._show_stimulus(i)
#
#     # Push end-trial marker
#     self.eeg.insert_marker(status='stop', label=self.labels[i], index=i)
#
# # Export and return the data
# trials = self._extract_trials()
# self.eeg.off()
