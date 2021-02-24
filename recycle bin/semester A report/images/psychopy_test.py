from psychopy import visual, core
import time
win = visual.Window()
cumulativeTimer = core.Clock()
width, height = [1, 0.15]
refresh_rate = 0.05
length = 5  # seconds

time_bar_frame = visual.Rect(win=win, pos=(0, 0), size=(width, height), lineColor='White')

time_bar = visual.Rect(win=win, pos=(0, 0), size=(0, height), fillColor='White')

cumulativeTimer.reset()

while True:

    time_bar.width = cumulativeTimer.getTime() / length
    time_bar.pos[0] = time_bar_frame.pos[0] - time_bar_frame.width / 2 + time_bar.width / 2
    time_bar_frame.draw()
    time_bar.draw()
    win.flip()

    time.sleep(refresh_rate)
