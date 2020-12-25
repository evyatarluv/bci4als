import sys
# test imports

from psychopy import visual,event
# end test imports

from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory


Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
print('try')
filename = askdirectory() # show an "Open" dialog box and return the path to the selected file
print(filename)
