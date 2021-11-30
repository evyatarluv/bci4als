import sys
import threading
import time
from PyQt5.QtWidgets import QApplication
from bci4als.eeg import EEG
from bci4als.ml_model import MLModel
from bci4als.mouse import VirtualMouse, MouseConfig


def control_mouse(config: MouseConfig, model_path: str):

    # Init variables
    model = MLModel(model_path=model_path)
    eeg = EEG(board_id=-1)
    vm = VirtualMouse(eeg=eeg, model=model, mouse_actions=config.mouse_actions)

    # Turn EEG on
    eeg.on()

    # Start controlling the virtual mouse
    while True:

        # Monitor the movement to indicate standstill
        vm.monitor(r=25, counter_limit=5, interval=0.4)

        # Predict the label imagined by the user
        label = vm.predict(buffer_time=4)

        # Convert the label to action according to current config
        action = config.get_action(label=label)

        # Execute the action
        vm.execute(action=action)


if __name__ == '__main__':

    # Init the app window
    app = QApplication(sys.argv)
    configuration = MouseConfig()
    clf_path = r'../../recordings/avi/4/model.pickle'

    # Start the virtual mouse
    threading.Thread(target=control_mouse,
                     args=(configuration, clf_path)).start()

    # Start the config window
    sys.exit(app.exec_())
