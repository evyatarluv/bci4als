import json
import typing
import matplotlib.pyplot as plt
import numpy

fpath = r"../recordings/avi/17/results.json"

data = json.load(open(fpath))


def trial_accuracy(trial: typing.List[typing.List[int]]):
    target = trial[0][0]
    n_attempts = len(trial)
    n_success = len([1 for t, p in trial if t == p])
    accuracy = n_success / n_attempts
    return accuracy


accuracies = [trial_accuracy(trial) for trial in data]

plt.plot(accuracies, label="accuracy")
plt.hlines(numpy.mean(accuracies), 0, len(data), colors='black',  linestyle='-', label="mean accuracy")
plt.hlines(0.2, 0, len(data), colors='black', linestyle='--', label="chance")
plt.xlabel("Trial Number")
plt.ylabel("Accuracy")
plt.title("Accuracies for Online Session (5 classes)")
plt.legend()
plt.text(0.05, numpy.mean(accuracies)+0.05, f"{round(numpy.mean(accuracies), 3)}")
# plt.yticks(list(plt.yticks()[0]) + [numpy.mean(accuracies)])
# plt.ylim((0,1))
plt.ylim(-0.05, 1.05)
plt.show()
