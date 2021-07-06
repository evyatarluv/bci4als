import json
import typing
import matplotlib.pyplot as plt
import numpy
import numpy as np


def trial_accuracy(trial: typing.List[typing.List[int]]):
    target = trial[0][0]
    n_attempts = len(trial)
    n_success = len([1 for t, p in trial if t == p])
    accuracy = n_success / n_attempts
    return accuracy


best_accuracies = []
errors = []

sessions = [7, 12, 13, 14, 15, 17, 21, 23]
for session_number in sessions:
    fpath = f"../recordings/avi/{session_number}/results.json"
    results = json.load(open(fpath))

    accuracies = [trial_accuracy(trial) for trial in results]

    plt.plot(accuracies, label="accuracy")
    plt.hlines(numpy.mean(accuracies), 0, len(results), colors='black', linestyle='-', label="mean accuracy")
    plt.hlines(0.2, 0, len(results), colors='black', linestyle='--', label="chance")
    plt.xlabel("Trial Number")
    plt.ylabel("Accuracy")
    # datetime =
    plt.title(f"Accuracies for Session {session_number}")
    plt.legend()
    plt.text(0.05, numpy.mean(accuracies) + 0.05, f"{round(numpy.mean(accuracies), 3)}")
    # plt.yticks(list(plt.yticks()[0]) + [numpy.mean(accuracies)])
    # plt.ylim((0,1))
    plt.ylim(-0.05, 1.05)
    plt.show()
    best_accuracies.append(numpy.mean(accuracies))
    errors.append(np.var(accuracies))
print(errors)
plt.errorbar(numpy.arange(1, len(best_accuracies) + 1), best_accuracies, yerr=errors, label="accuracy")
# plt.hlines(numpy.mean(best_accuracies), 0, len(best_accuracies), colors='black', linestyle='-', label="mean accuracy")
plt.hlines(0.2, 0, len(best_accuracies), colors='black', linestyle='--', label="chance")
plt.title(f"Mean Accuracy by Session")
plt.xlabel("Session Number")
plt.ylabel("Accuracy")
# plt.text(0.05, numpy.mean(best_accuracies) + 0.05, f"{round(numpy.mean(best_accuracies), 3)}")
plt.ylim(-0.05, 1.05)
# plt.xticks(numpy.arange(len(best_accuracies)), numpy.arange(1, len(best_accuracies) + 1))
plt.legend()
plt.show()
