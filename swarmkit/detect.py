"""
Detection of storm onsets and quiet/moderate/storm windows from DST.
"""
import numpy as np
import pandas as pd


def detect_onsets(dst, threshold=-50.0, min_sep_h=48, min_dur_h=6):
    """
    Detect storm onsets as local minima of DST below a threshold.

    Parameters
    ----------
    dst : pandas.Series
        DST index, indexed by UTC timestamp.
    threshold : float, default -50.0
        Minimum |DST| (nT) required for an onset.
    min_sep_h : int, default 48
        Minimum separation (hours) between successive onsets.
    min_dur_h : int, default 6
        Minimum duration (hours) below the threshold.

    Returns
    -------
    list of pandas.Timestamp
        Sorted list of onset times.
    """
    dst = dst.dropna()
    abaixo = dst[dst <= threshold]
    if abaixo.empty:
        return []

    grupos = (abaixo.index.to_series().diff()
              > pd.Timedelta(hours=min_sep_h)).cumsum()

    onsets = []
    for _, bloco in abaixo.groupby(grupos):
        dur = (bloco.index.max() - bloco.index.min()).total_seconds() / 3600
        if dur >= min_dur_h:
            onsets.append(bloco.idxmin())
    return sorted(onsets)


def classify_period(dst, t, thresholds=(-10, -50)):
    """
    Classify a time instant as calm, moderate, or storm.

    Parameters
    ----------
    dst : pandas.Series
        DST index, indexed by UTC timestamp.
    t : pandas.Timestamp
        Time of interest.
    thresholds : tuple, default (-10, -50)
        (calm_upper, storm_upper). Calm: DST > -10. Moderate:
        -50 < DST <= -10. Storm: DST <= -50.

    Returns
    -------
    str
        One of "calm", "moderate", "storm", or "unknown".
    """
    if t.tzinfo is None:
        t = t.tz_localize("UTC")

    window = dst[(dst.index >= t - pd.Timedelta(hours=1)) &
                 (dst.index <= t + pd.Timedelta(hours=1))]
    if window.empty:
        return "unknown"

    d = window.min()
    if pd.isna(d):
        return "unknown"
    if d > thresholds[0]:
        return "calm"
    elif d > thresholds[1]:
        return "moderate"
    return "storm"


def detect_windows(dst, target_state, min_dur_h=24,
                   min_sep_d=7, max_per_year=8):
    """
    Detect contiguous windows of a target geomagnetic state.

    Parameters
    ----------
    dst : pandas.Series
        DST index.
    target_state : {"calm", "moderate", "storm"}
        Which state to detect.
    min_dur_h : int, default 24
        Minimum duration of each window (hours).
    min_sep_d : int, default 7
        Minimum separation between window centers (days).
    max_per_year : int, default 8
        Maximum number of windows per calendar year.

    Returns
    -------
    pandas.DataFrame
        Columns: t_ini, t_fim, centro, dur_h, dst_min, dst_max.
    """
    if target_state == "calm":
        mask = (dst > -10)
    elif target_state == "moderate":
        mask = (dst > -50) & (dst < -10)
    elif target_state == "storm":
        mask = (dst < -50)
    else:
        raise ValueError("target_state must be calm, moderate or storm")

    mask = mask.astype(int)
    grupos = (mask.diff() != 0).cumsum()

    blocos = []
    for _, g in dst.groupby(grupos):
        if mask.loc[g.index[0]] != 1:
            continue
        dur_h = (g.index[-1] - g.index[0]).total_seconds() / 3600 + 1
        if dur_h >= min_dur_h:
            blocos.append(dict(
                t_ini=g.index[0],
                t_fim=g.index[-1],
                centro=g.index[len(g) // 2],
                dur_h=dur_h,
                dst_min=float(g.min()),
                dst_max=float(g.max()),
            ))

    df = pd.DataFrame(blocos)
    if df.empty:
        return df

    df = df.sort_values("centro").reset_index(drop=True)

    # Enforce minimum separation between window centers
    sel = []
    for _, b in df.iterrows():
        if not sel or (b["centro"] - sel[-1]["centro"]).total_seconds() / 86400 >= min_sep_d:
            sel.append(b)
    df = pd.DataFrame(sel).reset_index(drop=True)

    # Cap per year
    df["ano"] = df["centro"].dt.year
    df = (df.sort_values("centro")
            .groupby("ano")
            .head(max_per_year)
            .reset_index(drop=True))

    return df
