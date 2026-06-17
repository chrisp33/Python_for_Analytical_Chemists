# 2.2 — Indexing, Slicing, and Selecting Spectral Regions

**Title:** *Getting the Carbonyl Region, Not the Whole Spectrum*
**Track:** 2 — Scientific Computing · **Difficulty:** Beginner · **Length:** 12–14 min · **Type:** Core

## Learning objective

Select the part of a spectrum that carries the chemistry: grab single points and
slices, isolate a wavenumber region with a boolean mask, find the peak within it,
and exclude a detector gap.

## Why it matters

Real analysis happens in regions of interest — a fingerprint band, an analyte peak,
a quiet baseline window. Selecting by *value* (the chemistry) rather than by index
position keeps your code correct when the axis changes.

## What the notebook covers

1. Integer indexing and contiguous slicing, and why index positions are fragile.
2. Selecting a wavenumber region by value with a boolean mask.
3. Finding the peak within a region with `argmax`.
4. Excluding a detector gap by negating a mask (`~`).

## Prerequisites

- 2.1 (NumPy Arrays: Math on Whole Spectra at Once).

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. Produces one small figure; needs no external data.

## Data

Inline toy data only — an IR-style wavenumber axis with two Gaussian bands generated
with `numpy`. No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 2.2
- Follow-up: 2.3 — pandas DataFrames for Sample Tables
- YouTube: _(add link when published)_
