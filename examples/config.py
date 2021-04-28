import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap


class Config(QWidget):

    def __init__(self):
        super().__init__()

        # Window size and position
        self.left = 10
        self.top = 50
        self.width = 640
        self.height = 640

        # Widgets for the window
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.configs[self.current_config])

        # Config images params
        self.configs = [os.path.join('configs', img) for img in os.listdir('configs')]
        self.current_config = 0
        self.button_padding = {'bottom': 20, 'side': 10}

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Config()
    sys.exit(app.exec_())
