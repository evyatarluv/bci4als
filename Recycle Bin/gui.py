# test imports
import os
import sys
import time
from tkinter import Tk
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askdirectory

import numpy as np
import pandas as pd
import pylsl
from psychopy import visual, event
# end test imports

from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askdirectory() # show an "Open" dialog box and return the path to the selected file
print(filename)