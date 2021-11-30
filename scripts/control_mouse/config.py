import os
import sys
from typing import Optional
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap


class Config(QWidget):

    def __init__(self):
        super().__init__()

        # Window size and position
        self.left = 10
        self.top = 50
        self.width = 377
        self.height = 720

        # Config images params
        # self.configs = [os.path.join('configs', img) for img in os.listdir('configs')]
        # self.current_config = 0
        # self.button_padding = {'bottom': 20, 'side': 10}

        # Widgets for the window
        self.label = QLabel(self)
        # self.pixmap = QPixmap(self.configs[self.current_config])
        self.pixmap = QPixmap('pynput examples/configs/config.png')

        # # key = config image, value = actions
        # # assume: {0: 'right', 1: 'left', 2: 'idle', 3: 'tongue', 4: 'legs'}
        # self.config_dict = {0: {0: 'right_click', 1: 'left_click', 3: 'scroll_up', 4: 'scroll_down'},
        #                     1: {0: 'left_click', 1: 'left_release', 3: 'scroll_up', 4: 'scroll_down'},
        #                     2: {0: 'right_click', 1: 'double_click', 3: 'scroll_up', 4: 'scroll_down'}}

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

        # # Next button
        # next_button = QPushButton(self)
        # next_button.setText('Next')
        # next_button.clicked.connect(self.next_config)
        # next_button.move(self.width - next_button.width() - self.button_padding['side'] * 2,
        #                  self.height - next_button.height() - self.button_padding['bottom'])
        #
        # # Previous button
        # previous_button = QPushButton(self)
        # previous_button.setText('Previous')
        # previous_button.clicked.connect(self.previous_config)
        # previous_button.move(self.button_padding['side'],
        #                      self.height - next_button.height() - self.button_padding['bottom'])

        # Combo-box
        space = 170
        x, y = 230, 85
        for i in range(5):
            cb = QComboBox(self)
            cb.addItems(['Right Click', 'Left Click', 'Double Click', 'Ctrl + C', 'Ctrl + V', 'Left Press',
                        'Left Release', 'None'])
            cb.move(x, y + i * space)

        self.show()

    def get_action(self, label: int) -> str:
        """
        The method get the ML model prediction and returns the action which need to be actioned by the mouse
        according to the current configuration on the screen.
        :param label: prediction of the ML model - 0-> right, 1-> left, 2-> idle, 3-> tongue, 4-> legs
        :return: action of the mouse as str
        """
        return self.config_dict[self.current_config][label]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Config()
    sys.exit(app.exec_())
