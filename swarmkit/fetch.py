"""
Data access for Swarm (VirES) and OMNI (NASA/SPDF).
"""
import time
from io import StringIO
import urllib.request
import numpy as np
import pandas as pd


VIRES_URL = "https://vires.services/ows"
OMNI_BASE = "https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni"

COLECOES = {
    "A": "SW_OPER_MAGA_LR_1B",
    "B": "SW_OPER_MAGB_LR_1B",
    "C": "SW_OPER_MAGC_LR_1B",
}


def fetch_swarm_window(sat, t0, t1, retries=3, backoff=45):
    """
    Download one Swarm window for a given satellite.

    Parameters
    ----------
    sat : {"A", "B", "C"}
        Swarm satellite identifier.
    t0, t1 : str
        ISO8601 timestamps (e.g., "2024-05-10T00:00:00Z").
    retries : int, default 3
        Number of retry attempts.
    backoff : int, default 45
        Seconds between retries (multiplied by attempt number).

    Returns
    -------
    pandas.DataFrame
        DataFrame with F, B_NEC, Flags_F, Flags_B, Latitude, Longitude,
        Radius, Spacecraft. Index is timezone-aware UTC.

    Notes
    -----
    Swarm Charlie (C) does not carry an absolute scalar magnetometer,
    so the `F` column will be NaN for satellite C. Use `|B_NEC|`
    instead for vector-only analysis.
    """
    from viresclient import SwarmRequest

    if sat not in COLECOES:
        raise ValueError(f"sat must be one of {list(COLECOES)}")

    last = None
    for k in range(retries):
        try:
            req = SwarmRequest(VIRES_URL)
            req.set_collection(COLECOES[sat])
            req.set_products(
                measurements=["F", "B_NEC", "Flags_F", "Flags_B"],
                auxiliaries=["Latitude", "Longitude", "Radius", "Spacecraft"],
            )
            df = req.get_between(t0, t1).as_dataframe()
            if df.index.tz is None:
                df = df.tz_localize("UTC")
            else:
                df = df.tz_convert("UTC")
            return df
        except Exception as ex:
            last = ex
            time.sleep(backoff * (k + 1))
    raise last


def download_omni(year):
    """
    Download one year of OMNI2 hourly data.

    Parameters
    ----------
    year : int
        Year (e.g., 2024).

    Returns
    -------
    pandas.DataFrame
        Indexed by UTC timestamp, with columns `dst` and `ae`.
    """
    url = f"{OMNI_BASE}/omni2_{year}.dat"
    with urllib.request.urlopen(url, timeout=60) as r:
        raw = pd.read_csv(StringIO(r.read().decode()), sep=r"\s+",
                          header=None, engine="python")

    omni = pd.DataFrame({
        "timestamp": pd.to_datetime(raw[0].astype(str) + "-01-01", utc=True)
                     + pd.to_timedelta(raw[1] - 1, unit="D")
                     + pd.to_timedelta(raw[2], unit="h"),
        "dst": raw[40].astype(float),
        "ae": raw[41].astype(float),
    })
    omni.loc[omni["dst"] >= 9999, "dst"] = np.nan
    omni.loc[omni["ae"] >= 9999, "ae"] = np.nan

    return omni.set_index("timestamp").sort_index()


def load_omni_multi(start_year, end_year):
    """
    Download OMNI2 for a range of years and concatenate.

    Parameters
    ----------
    start_year, end_year : int
        Inclusive range.

    Returns
    -------
    pandas.DataFrame
        Concatenated OMNI data.
    """
    frames = [download_omni(y) for y in range(start_year, end_year + 1)]
    return pd.concat(frames).sort_index()
