# 2.8 — Reshaping Data for Analysis

**Title:** *One Row per Spectrum: Reshaping for Analysis*
**Track:** 2 — Scientific Computing · **Difficulty:** Intermediate · **Length:** 14–16 min · **Type:** Core

## Learning objective

Move data between long and wide layouts and assemble a samples-by-wavelengths matrix:
pivot long → wide, melt wide → long, and hand a clean numeric matrix to a model.

## Why it matters

Chemometric and machine-learning tools expect one row per sample and one column per
wavelength. Data often arrives long (one row per point); reshaping it into that
matrix is half the battle before any modelling.

## What the notebook covers

1. Recognizing long (tidy) vs wide layouts.
2. `pivot` to turn a long table into a samples-by-wavelengths matrix.
3. `melt` to reverse the reshape.
4. `.to_numpy()` to produce the model-ready matrix while keeping IDs and wavelengths.

## Prerequisites

- 2.3 (pandas DataFrames for Sample Tables); 2.7 for getting joined data first.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. It needs no external data.

## Data

Inline toy data only — three small spectra in long format typed into the notebook. No
external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 2.8
- Previous: 2.7 — Joining Measurements and Metadata
- Follow-up: 3.1 — Noise, Signal, and What Smoothing Really Does (Track 3)
- YouTube: _(add link when published)_
