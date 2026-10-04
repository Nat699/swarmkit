# swarmkit

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

**SAMA signature detection from Swarm magnetic field data.**

`swarmkit` is a Python library for detecting and quantifying the signature of the South Atlantic Magnetic Anomaly (SAMA) in scalar magnetic field data from ESA's Swarm satellites during geomagnetic storms.

## Key result

The SAMA amplifies the skewness of the scalar magnetic field `F` during storms, with a **threshold activation at DST ≈ −49 nT**. The effect is satellite-invariant (Swarm A and B), absent during quiet times, and specific to the anomaly (verified against a control region at the same latitude).

| Metric | Value |
|---|---|
| Classification AUC (5-fold CV) | **0.9993 ± 0.0008** |
| Δskew (SAMA − control, storm) | **+0.71** |
| Δskew (SAMA − control, calm) | +0.08 |
| Threshold | DST ≈ −49 nT |
| ΔAIC (step vs. linear) | **+48.6** |

This work is described in the manuscript submitted to *Geophysical Research Letters* (2026GL127373).

## Installation

```bash
pip install git+https://github.com/Nat699/swarmkit.git
