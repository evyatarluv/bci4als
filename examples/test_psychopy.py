from psychopy import visual, event
from bci4als.learning.online import Feedback

# Some parameters.
RISE_SPEED = 0.02  # how much to increase width in each frame. (here 2% increase every frame)
RISE_END = 1.45   # end animation at this unit width

# # Set up the window and bar.
# win = visual.Window()
#
# # Set up other elements
# progress_bar = visual.Rect(win, width=0, height=0.2, pos=(0, 0), lineColor='black', fillColor='green')
# center_line = visual.Rect(win, pos=(0, 0), lineColor=None, fillColor='black', width=0.01, height=0.4)
# bar_frame = visual.Rect(win, pos=(0, 0), lineColor='black', fillColor=None, width=1.9, height=0.2)
#
# # While the height is less than RISE_END.
# while progress_bar.width < RISE_END:
#
#     # Increase the height (y-length in both directions) and then move up on Y so that the base stays put.
#     progress_bar.width += RISE_SPEED
#     # progress_bar.pos[0] += progress_bar.width * RISE_SPEED / 2  # the y-position only
#     progress_bar.pos[0] += RISE_SPEED / 2
#
#     # Show it.
#     progress_bar.draw()
#     center_line.draw()
#     bar_frame.draw()
#     win.flip()
#
#     # Wait
#     event.waitKeys()

f = Feedback(0)
f._display()
