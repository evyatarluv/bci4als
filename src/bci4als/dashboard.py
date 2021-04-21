from typing import List


class Dashboard:

    def __init__(self):
        pass

    def confidence_plot(self, ax, labels: List[str], confidence: List[float]):

        ax.clear()
        ax.bar([l.capitalize() for l in labels], confidence, color='lightblue')
        ax.set_title('Confidence')
        ax.set_ylim(-20, 20)

        return ax

    def accuracy_plot(self, ax, accuracy: float, label: str):

        ax.clear()
        ax.bar(['Accuracy'], accuracy, color='limegreen')
        ax.set_title(f'Accuracy: Predict = {label}')
        ax.set_ylim(0, 1)

        return ax

