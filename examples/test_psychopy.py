from psychopy import visual, event
from bci4als.learning.online import Feedback

win = visual.Window(fullscr=False)

f = Feedback(win, 1)

f.update(1)
event.waitKeys()
f.update(1)
event.waitKeys()
