# 2.1 — NumPy Arrays: Math on Whole Spectra at Once

**Title:** *Doing the Same Math to a Thousand Spectra at Once*
**Track:** 2 — Scientific Computing · **Difficulty:** Beginner · **Length:** 14–16 min · **Type:** Core

## Learning objective

Do arithmetic on whole spectra at once: subtract a baseline from a thousand spectra
in one line, and summarize a batch with array reductions — without writing loops.

## Why it matters

Vectorized math is how you baseline-subtract a tray of spectra in one expression
instead of one at a time, and it mirrors how you think about signals mathematically.
It is the foundation every later preprocessing step is built on.

## What the notebook covers

1. Whole-array arithmetic on a single spectrum (scalar and element-wise).
2. A stack of spectra as a 2-D array (rows = spectra, columns = wavelengths).
3. Baseline-correcting 1000 spectra in one line via broadcasting.
4. Reductions: mean spectrum (`axis=0`), per-spectrum peak (`axis=1`), averaging replicates.

## Prerequisites

- 1.6 (Functions) and the Track 1 foundations; 1.4 (Lists, Arrays, and a First Spectrum)
  in particular.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. Produces one small figure; needs no external data.

## Data

Inline toy data only — a wavelength axis and spectra generated with `numpy` (fixed
seed). No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 2.1
- Follow-up: 2.2 — Indexing, Slicing, and Selecting Spectral Regions
- YouTube: _(add link when published)_
