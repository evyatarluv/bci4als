import time
from pynput.mouse import Button, Controller
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap


class MouseConfig(QWidget):

    def __init__(self):
        super().__init__()

        # Window size and position
        self.left = 10
        self.top = 50
        self.width = 640
        self.height = 640

        # Config images params
        config_folder = os.path.join(os.path.dirname(__file__), 'configs')
        self.configs = [os.path.join(config_folder, img) for img in os.listdir(config_folder)]
        self.current_config = 0
        self.button_padding = {'bottom': 20, 'side': 10}

        # key = config image, value = actions
        # assume: {0: 'right', 1: 'left', 2: 'idle', 3: 'tongue', 4: 'legs'}
        self.config_dict = {0: {0: 'right_click', 1: 'left_click', 3: 'scroll_up', 4: 'scroll_down'},
                            1: {0: 'left_hold', 1: 'left_release', 3: 'scroll_up', 4: 'scroll_down'},
                            2: {0: 'right_click', 1: 'double_click', 3: 'scroll_up', 4: 'scroll_down'}}

        # Widgets for the window
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.configs[self.current_config])

        # Init window
        self.initUI()

    def next_config(self):

        # Change current config index
        if self.current_config + 1 == len(self.configs):
            self.current_config = 0
        else:
            self.current_config += 1

        # Change the image
        self.pixmap = QPixmap(self.configs[self.current_config])
        self.label.setPixmap(self.pixmap)

    def previous_config(self):

        # Change current config index
        if self.current_config - 1 == -1:
            self.current_config = len(self.configs) - 1
        else:
            self.current_config -= 1

        # Change the image
        self.pixmap = QPixmap(self.configs[self.current_config])
        self.label.setPixmap(self.pixmap)

    def initUI(self):

        # Set title & position
        self.setWindowTitle('BCI Configuration')
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Configuration image
        self.label.setPixmap(self.pixmap)

        # Next button
        next_button = QPushButton(self)
        next_button.setText('Next')
        next_button.clicked.connect(self.next_config)
        next_button.move(self.width - next_button.width() - self.button_padding['side'] * 2,
                         self.height - next_button.height() - self.button_padding['bottom'])

        # Previous button
        previous_button = QPushButton(self)
        previous_button.setText('Previous')
        previous_button.clicked.connect(self.previous_config)
        previous_button.move(self.button_padding['side'],
                             self.height - next_button.height() - self.button_padding['bottom'])

        self.show()

    def get_action(self, label: int) -> str:
        """
        The method get the ML model prediction and returns the action which need to be actioned by the mouse
        according to the current configuration on the screen.
        :param label: prediction of the ML model - 0-> right, 1-> left, 2-> idle, 3-> tongue, 4-> legs
        :return: action of the mouse as str
        """
        return self.config_dict[self.current_config][label]


def movement_indicator(r: float, counter_limit: int, interval: float) -> bool:
    """

    :param r:
    :param counter_limit:
    :param interval:
    :return:
    """

    mouse = Controller()
    x_center, y_center = mouse.position
    counter = 0

    while counter < counter_limit:

        x, y = mouse.position

        if ((x - x_center) ** 2) + ((y - y_center) ** 2) < r ** 2:

            counter += 1
            print(f'Counter: {counter}')
        else:

            x_center, y_center = x, y
            counter = 0

        time.sleep(interval)

    return True


def execute_action(action: str):

    mouse = Controller()

    # Click action
    if 'click' in action:

        if 'right' in action:
            mouse.press(Button.right)
            mouse.release(Button.right)

        elif 'left' in action:
            mouse.press(Button.left)
            mouse.release(Button.left)

        elif 'double' in action:
            mouse.click(Button.left, 2)

    # Press action
    elif 'hold' in action:

        if 'left' in action:
            mouse.press(Button.right)

    # Realse action
    elif 'release' in action:

        if 'left' in action:
            mouse.release(Button.left)

    # Scroll action
    elif 'scroll' in action:

        if 'down' in action:
            mouse.scroll(0, 2)

        elif 'up' in action:
            mouse.scroll(0, -2)

    # If unknown action raise exception
    elif action is not None:
        raise NotImplementedError('The given action is not supprted')
