import sys
import threading
from PyQt5.QtWidgets import QApplication
from bci4als.mouse import VirtualMouse, MouseConfig


def control_mouse(config: MouseConfig):

    virtual_mouse = VirtualMouse(config)

    while True:

        virtual_mouse.monitor(r=25, counter_limit=5, interval=0.4)

        action = config.get_action(label=1)  # todo: `label` arg need to be the ML model prediction

        virtual_mouse.execute(action=action)


if __name__ == '__main__':

    # Init the app window
    app = QApplication(sys.argv)
    configuration = MouseConfig()

    # Start the virtual mouse
    threading.Thread(target=control_mouse, args=(configuration,)).start()

    # Start the config window
    sys.exit(app.exec_())
