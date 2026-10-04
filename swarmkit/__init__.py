"""
swarmkit — SAMA signature detection from Swarm magnetic field data.

Quick start:
    from swarmkit import SamaClassifier, extract_features

    clf = SamaClassifier.load("model.pkl")
    p = clf.predict_proba(F_series)
"""

__version__ = "0.1.0"

from .model import SamaClassifier
from .features import extract_features, SHAPE_FEATURES
from .detect import detect_onsets, detect_windows, classify_period
from .fetch import fetch_swarm_window, download_omni

__all__ = [
    "SamaClassifier",
    "extract_features",
    "SHAPE_FEATURES",
    "detect_onsets",
    "detect_windows",
    "classify_period",
    "fetch_swarm_window",
    "download_omni",
]
