from bci4als.mouse import movement_indicator, mouse_action
import easygui


for i in range(10):

    movement_indicator(r=25, counter_limit=5, interval=0.5)

    mouse_action(1)
