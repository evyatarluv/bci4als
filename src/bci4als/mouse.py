import time
from pynput.mouse import Button, Controller


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


def mouse_action(label: int):

    mouse = Controller()

    mouse.click(Button.left, 2)

