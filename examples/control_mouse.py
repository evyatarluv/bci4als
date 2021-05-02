import sys
import threading
from PyQt5.QtWidgets import QApplication
from bci4als.mouse import movement_indicator, execute_action, MouseConfig


def control_mouse(config: MouseConfig):

    for i in range(10):

        movement_indicator(r=25, counter_limit=5, interval=0.4)

        action = config.get_action(label=1)  # todo: `label` arg need to be the ML model prediction

        execute_action(action=action)


# Turn the configuration window on
app = QApplication(sys.argv)
configuration = MouseConfig()

threading.Thread(target=control_mouse, args=(configuration,)).start()

sys.exit(app.exec_())
