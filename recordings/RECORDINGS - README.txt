*******************************

July 6th 2021

*******************************

bci4als - Team 4 - EEG Recordings - ReadME

*******************************

Hello!

We hope you enjoy working on the bci4als project as much as we did.

Each folder is produced at the end of a recording session, and includes:
1) The EEG data split into trials, before processing.
2) The labels.
3) metadata.txt file with info about the recording.
4) results.json (target and prediction pairs, only for online recordings).

The way to load a pickle file is:
+++++++++++++++++++++++++++++++++
import pickle
fpath = '<PATH TO FILE HERE>'
d = pickle.load(open(fpath, 'rb'))
++++++++++++++++++++++++++++++++++

In some of the later folders, the trials and labels are put together into the model.pickle file.

Use the `test` folder when you are testing the bci4als system, and don't really care about the data.