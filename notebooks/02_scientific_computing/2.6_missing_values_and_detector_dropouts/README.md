# 2.6 — Missing Values and Detector Dropouts

**Title:** *When the Detector Hands You a Hole in the Data*
**Track:** 2 — Scientific Computing · **Difficulty:** Intermediate · **Length:** 14–16 min · **Type:** Core

## Learning objective

Handle missing values as measurement events: find and count them, distinguish a
dropout from a saturation from a dead channel, and choose drop vs interpolate vs
flag with the consequences in mind.

## Why it matters

A `NaN` is not a nuisance to silence — it records that the instrument did not return
a trustworthy value. Drop, interpolate, and flag each change the result differently,
so the choice is a scientific one, not a coding convenience.

## What the notebook covers

1. Where NaNs come from: detector dropouts, saturated pixels, dead channels.
2. Detecting and counting missing values (`np.isnan`, `df.isna().sum()`).
3. Treating saturation as wrong-high, not missing — converting clipped points to `NaN`.
4. Drop vs interpolate vs flag, with the scientific consequence of each, including
   why interpolating across a peak biases area and height.

## Prerequisites

- 2.3 (pandas DataFrames for Sample Tables); 2.1 for array basics.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. Produces one small figure; needs no external data.

## Data

Inline toy data only — a short spectrum with two dropouts and one saturated point,
typed into the notebook. No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 2.6
- Follow-up: 2.7 — Joining Measurements and Metadata
- YouTube: https://youtu.be/qgoFJGtNAto

> **Note for maintainers:** this lesson's topic (Missing Values and Detector
> Dropouts) supersedes the older curriculum placeholder for 2.6 ("Tidy Data and
> Reshaping Spectral Matrices"); reshaping now lives in 2.8. See `docs/STATUS.md`.
