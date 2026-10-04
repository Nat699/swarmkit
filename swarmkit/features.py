"""
Feature extraction for SAMA classification.
"""
import numpy as np
from scipy import stats, signal


def extract_features(F, fs=1.0):
    """
    Extract 18 features from a scalar magnetic field series.

    Parameters
    ----------
    F : array-like
        Scalar magnetic field samples (nT).
    fs : float, default 1.0
        Sampling frequency in Hz.

    Returns
    -------
    dict or None
        Feature dictionary, or None if the segment is too short.

    Notes
    -----
    Features are grouped into three categories:
        - Level (6): mean, median, p25, p75, min, max
        - Shape (6): std, ptp, skew, kurt, sum|dz|, sum dz^2
        - Spectral (6): Welch PSD in six bands (0-0.5 Hz)
    """
    F = np.asarray(F, dtype=np.float64)
    if len(F) < 10:
        return None

    mu, sd = F.mean(), F.std() + 1e-9
    z = (F - mu) / sd

    fr, ps = signal.welch(z, fs=fs, nperseg=min(512, len(z)))
    bands = [(0, 0.01), (0.01, 0.05), (0.05, 0.1),
             (0.1, 0.2), (0.2, 0.35), (0.35, 0.5)]

    psd_vals = []
    for lo, hi in bands:
        m = (fr >= lo) & (fr < hi)
        psd_vals.append(float(np.trapz(ps[m], fr[m])) if m.any() else 0.0)

    return dict(
        mean=float(mu),
        std=float(sd),
        min=float(F.min()),
        max=float(F.max()),
        ptp=float(F.ptp()),
        skew=float(stats.skew(F)),
        kurt=float(stats.kurtosis(F)),
        median=float(np.median(F)),
        p25=float(np.percentile(F, 25)),
        p75=float(np.percentile(F, 75)),
        sum_abs_dz=float(np.sum(np.abs(np.diff(z)))),
        sum_dz2=float(np.sum(np.diff(z) ** 2)),
        psd_0_001=psd_vals[0],
        psd_001_005=psd_vals[1],
        psd_005_01=psd_vals[2],
        psd_01_02=psd_vals[3],
        psd_02_035=psd_vals[4],
        psd_035_05=psd_vals[5],
    )


SHAPE_FEATURES = [
    "std", "ptp", "skew", "kurt",
    "sum_abs_dz", "sum_dz2",
    "psd_0_001", "psd_001_005", "psd_005_01",
    "psd_01_02", "psd_02_035", "psd_035_05",
]

LEVEL_FEATURES = ["mean", "median", "p25", "p75", "min", "max"]
