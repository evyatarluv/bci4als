from psychopy import visual, event

# Some parameters.
RISE_SPEED = 0.02  # how much to increase width in each frame. (here 2% increase every frame)
RISE_END = 1.0  # end animation at this unit width

# Set up the window and bar.
win = visual.Window()
progress_bar = visual.Rect(win, width=0.1, height=0.2, pos=(0, 0),
                           lineColor='black',
                           fillColor='green')
# right_line = visual.Line(win, height=)

# While the height is less than RISE_END.
while progress_bar.width < RISE_END:
    # Increase the height (y-length in both directions) and then move up on Y so that the base stays put.
    progress_bar.width += RISE_SPEED
    # progress_bar.pos[0] += progress_bar.width * RISE_SPEED / 2  # the y-position only
    progress_bar.pos[0] += RISE_SPEED / 2

    # Show it.
    progress_bar.draw()
    win.flip()

    # Wait
    event.waitKeys()

