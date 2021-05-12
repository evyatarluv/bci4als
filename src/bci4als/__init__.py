"""Top-level package for BCI-4-ALS."""
import importlib_metadata

__author__ = """Evyatar Luvaton, Noam Siegel"""
__email__ = 'noamsi@post.bgu.ac.il'
__version__ = importlib_metadata.version('bci4als')

from bci4als.experiments.offline import OfflineExperiment
from bci4als.experiments.online import OnlineExperiment
from .eeg import EEG
from .ml_model import MLModel
