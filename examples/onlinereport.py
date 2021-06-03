import json
import typing
import matplotlib.pyplot as plt
import numpy

fpath = r"../recordings/avi/15/results.json"

data = json.load(open(fpath))


def trial_accuracy(trial: typing.List[typing.List[int]]):
    target = trial[0][0]
    n_attempts = len(trial)
    n_success = len([1 for t, p in trial if t == p])
    accuracy = n_success / n_attempts
    return accuracy


accuracies = [trial_accuracy(trial) for trial in data]

plt.plot(accuracies, label="trials")
plt.hlines(numpy.mean(accuracies), 0, len(data), colors='black', label="mean")
plt.xlabel("Trial Number")
plt.ylabel("Accuracy")
plt.title("Accuracies for Online Session")
plt.legend()
plt.show()
