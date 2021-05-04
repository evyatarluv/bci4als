import pickle
import sys
import threading
from PyQt5.QtWidgets import QApplication
from bci4als.mouse import VirtualMouse, MouseConfig


def predict_label(model):
    # todo: fill up this function - ML model predict the label of the user
    return 1


def control_mouse(config: MouseConfig):

    virtual_mouse = VirtualMouse(config)
    model = pickle.load(open(r'models/7/sgd.pkl', 'rb'))

    while True:

        # Monitor the movement to indicate standstill
        virtual_mouse.monitor(r=25, counter_limit=5, interval=0.4)

        # Predict the label imagined by the user
        label = predict_label(model)

        # Convert the label to action according to current config
        action = config.get_action(label=label)

        # Execute the action
        virtual_mouse.execute(action=action)


if __name__ == '__main__':

    # Init the app window
    app = QApplication(sys.argv)
    configuration = MouseConfig()

    # Start the virtual mouse
    threading.Thread(target=control_mouse, args=(configuration,)).start()

    # Start the config window
    sys.exit(app.exec_())
