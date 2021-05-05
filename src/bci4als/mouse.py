import os
import time
from typing import Optional, List
from PyQt5.QtCore import Qt
from pynput.mouse import Button
from pynput.mouse import Controller as Controller_mouse
from pynput.keyboard import Key
from pynput.keyboard import Controller as Controller_keyboard
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox
from PyQt5.QtGui import QPixmap, QFont


class MouseConfig(QWidget):

    def __init__(self):
        super().__init__()

        # Window size and position
        self.left = 10
        self.top = 10
        self.width = 415
        self.height = 770

        # Widgets for the window
        self.label = QLabel(self)
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'configs', 'config.png'))

        # Combo-box
        self.mouse_actions = ['Scroll Up', 'Right Click', 'Left Click', 'Scroll Down',
                              'Double Click', 'Ctrl + C', 'Ctrl + V', 'Left Press',
                              'Left Release', 'None']
        self.box_x = 265
        self.box_y = [85, 270, 450, 665]
        self.boxes = []
        self.box_font = QFont('Calibri', 10)

        # Init window
        self.initUI()

    def initUI(self):

        # Set window properties
        self.setWindowTitle('Config')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Configuration image
        self.label.setPixmap(self.pixmap)

        # Set combo boxes
        for i in range(4):
            cb = QComboBox(self)
            cb.addItems(self.mouse_actions)
            cb.setCurrentText(self.mouse_actions[i])
            cb.move(self.box_x, self.box_y[i])
            cb.setFont(self.box_font)
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
        # 0 - tongue, 1 - right, 2 - left, 3 - legs
        config_dict = {0: 1, 1: 2, 3: 0, 4: 3}

        if label == 2:  # idle
            return None
        else:
            return str(self.boxes[config_dict[label]].currentText())


class VirtualMouse:

    def __init__(self, config: MouseConfig):

        self.mouse = Controller_mouse()
        self.keyboard = Controller_keyboard()
        self.actions = {'right click': self.right_click, 'left click': self.left_click,
                        'double click': self.double_click, 'ctrl + c': self.ctrl_c, 'ctrl + v': self.ctrl_v,
                        'left press': self.left_press, 'left release': self.left_release,
                        'scroll up': self.scroll_up, 'scroll down': self.scroll_down}

        # Assert all actions from the config object exist in the virtual mouse object
        self.assert_actions(config.mouse_actions)

    def assert_actions(self, config_actions: List[str]):
        """
        The method assert all the action in ConfigMouse exist in VirtualMouse
        :param config_actions: list with all the actions which represent to user
        :return:
        """
        for a in config_actions:

            if (a is not 'None') and (a.lower() not in self.actions.keys()):

                raise ValueError(f'The action `{a}` is in ConfigMouse but not implemented in VirtualMouse')

    def monitor(self, r: float, counter_limit: int, interval: float) -> bool:

        x_center, y_center = self.mouse.position
        counter = 0

        while counter < counter_limit:

            x, y = self.mouse.position

            if ((x - x_center) ** 2) + ((y - y_center) ** 2) < r ** 2:

                counter += 1
                print(f'Counter: {counter}')
            else:

                x_center, y_center = x, y
                counter = 0

            time.sleep(interval)

        return True

    def execute(self, action: str):
        """
        The method execute the given action
        :param action: the action to execute as str
        :return:
        """

        if action is not None:

            self.actions[action.lower()]()

    def right_click(self):
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)

    def left_click(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def double_click(self):
        self.mouse.click(Button.left, 2)

    def left_press(self):
        self.mouse.press(Button.right)

    def left_release(self):
        self.mouse.release(Button.left)

    def scroll_up(self):
        self.mouse.scroll(0, -2)

    def scroll_down(self):
        self.mouse.scroll(0, 2)

    def ctrl_c(self):

        # Choose the file under the cursor
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

        # ctrl+c it!
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')

    def ctrl_v(self):

        # Choose the file under the cursor
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

        # ctrl+v it!
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('v')
            self.keyboard.release('v')
