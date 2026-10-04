"""
SamaClassifier — detect the SAMA signature in a magnetic field series.
"""
import pickle
import numpy as np
import pandas as pd
from .features import extract_features, SHAPE_FEATURES


class SamaClassifier:
    """
    Binary classifier: point inside vs. outside the SAMA.

    Wraps a scikit-learn estimator trained on shape features
    (std, ptp, skew, kurt, sum|dz|, sum dz^2, PSD bands) extracted
    from 1500-sample windows of scalar magnetic field.

    Parameters
    ----------
    model : sklearn estimator or None
        Trained model with a `predict_proba` method. If None, the
        classifier returns 0.5 for any input (fallback).

    Examples
    --------
    >>> clf = SamaClassifier.load("rf_sama.pkl")
    >>> p = clf.predict_proba(F_series)
    """

    def __init__(self, model=None):
        self.model = model

    @classmethod
    def load(cls, path):
        """Load a pickled scikit-learn model from disk."""
        with open(path, "rb") as fh:
            return cls(model=pickle.load(fh))

    def save(self, path):
        """Save the wrapped scikit-learn model to disk."""
        with open(path, "wb") as fh:
            pickle.dump(self.model, fh)

    def predict_proba(self, F_series):
        """
        Probability that the given series lies inside the SAMA.

        Parameters
        ----------
        F_series : array-like
            Scalar magnetic field samples.

        Returns
        -------
        float
            Probability in [0, 1]. Returns 0.5 if the model is missing
            or the segment is too short.
        """
        feats = extract_features(F_series)
        if feats is None or self.model is None:
            return 0.5
        X = np.array([[feats[k] for k in SHAPE_FEATURES]])
        return float(self.model.predict_proba(X)[0, 1])

    def predict(self, F_series, threshold=0.5):
        """Binary prediction using the given probability threshold."""
        return self.predict_proba(F_series) >= threshold

    def predict_many(self, segments):
        """Vectorized prediction over a list of segments."""
        return [self.predict_proba(s) for s in segments]
