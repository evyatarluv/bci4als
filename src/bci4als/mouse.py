import time
from typing import Optional

from pynput.mouse import Button
from pynput.mouse import Controller as Controller_mouse
from pynput.keyboard import Key
from pynput.keyboard import Controller as Controller_keyboard
import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap


class MouseConfig(QWidget):

    def __init__(self):
        super().__init__()

        # Window size and position
        self.left = 10
        self.top = 50
        self.width = 377
        self.height = 720

        # Widgets for the window
        self.label = QLabel(self)
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'configs', 'config.png'))

        # Combo-box
        self.mouse_actions = ['Right Click', 'Left Click', 'Double Click', 'Ctrl + C', 'Ctrl + V', 'Left Press',
                              'Left Release', 'None']
        self.box_space = 170
        self.box_init_pos = (230, 85)
        self.boxes = []

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

        # Set combo boxes
        for i in range(5):
            cb = QComboBox(self)
            cb.addItems(['Right Click', 'Left Click', 'Double Click', 'Ctrl + C', 'Ctrl + V', 'Left Press',
                        'Left Release', 'None'])
            cb.move(self.box_init_pos[0], self.box_init_pos[1] + i * self.box_space)
            self.boxes.append(cb)

        self.show()

    def get_action(self, label: int) -> Optional[str]:
        """
        The method get the ML model prediction and returns the action which need to be actioned by the mouse
        according to the current configuration on the screen.
        :param label: prediction of the ML model - 0-> right, 1-> left, 2-> idle, 3-> tongue, 4-> legs
        :return: action of the mouse as str
        """
        # According the config img locations
        # 0 - right, 1 - left, 2 - tongue, 3 - legs
        config_dict = {0: 0, 1: 1, 3: 2, 4: 3}

        if label == 2:  # idle
            return None
        else:
            return str(self.boxes[config_dict[label]].currentText())


def movement_indicator(r: float, counter_limit: int, interval: float) -> bool:
    """

    :param r:
    :param counter_limit:
    :param interval:
    :return:
    """

    mouse = Controller_mouse()
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

    mouse = Controller_mouse()
    action = action.lower()

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


def ctrl_c():

    mouse = Controller_mouse()
    keyboard = Controller_keyboard()

    # Choose the file under the cursor
    mouse.press(Button.left)
    mouse.release(Button.left)

    # ctrl+c it!
    with keyboard.pressed(Key.ctrl):
        keyboard.press('c')
        keyboard.release('c')


def ctrl_v():

    mouse = Controller_mouse()
    keyboard = Controller_keyboard()

    # Choose the file under the cursor
    mouse.press(Button.left)
    mouse.release(Button.left)

    # ctrl+v it!
    with keyboard.pressed(Key.ctrl):
        keyboard.press('v')
        keyboard.release('v')
