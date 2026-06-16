# 2.4 — Reading Real Instrument Files (CSV, TXT, and the Messy Ones)

**Title:** *Getting Your Instrument Data Into Python (Without Losing Your Mind)*
**Track:** 2 — Scientific Computing · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Foundation

## Learning objective

Import exported spectra and chromatograms reliably: skip metadata headers, parse
non-standard delimiters and decimal separators, drop footer junk, handle missing
values, and verify the data is correct once it's loaded.

## Why it matters

The first wall every scientist hits is a file that won't load cleanly. Vendor
software exports for its own convenience, not for pandas — so you get header
junk, semicolons, comma decimals, footers, and `N/A`s. A misparse rarely throws
an error; it silently corrupts every downstream calibration and model. Reading
the file correctly *is* part of the measurement.

## What the notebook covers

1. **Look before you load** — inspect raw lines with `repr()` before parsing.
2. Skip metadata headers (`skiprows`), drop footers (`skipfooter`) and comments
   (`comment`).
3. Non-standard formats: `sep=';'`, `decimal=','`, whitespace (`\s+`), `na_values`.
4. Clean + inspect: dtype checks, monotonic-axis and physical-range sanity checks.
5. A reusable `load_spectrum()` that auto-sniffs delimiter and header.
6. Verify every parse against the simulated ground truth with `np.allclose`.

Four deliberately messy export files are generated inside the notebook (into
`exports/`, git-ignored) so the lesson is fully self-contained and reproducible.

## Prerequisites

- 2.3 (pandas DataFrames) — briefly inlined.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create
and activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. When
the notebook opens, select the `.venv` kernel — and **restart the kernel if you
just installed the package** (see [Troubleshooting](../../../README.md#troubleshooting)).

Open and run this notebook from this folder (top to bottom). It needs no
external data — everything is generated from a fixed random seed, so your output
matches the committed output exactly. The `exports/` folder it creates is
regenerable scratch and is git-ignored.

## Data

Simulated UV-Vis spectra via `from simulated_data import uvvis` (`seed=7`). No
external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 2.4
- Follow-up: 2.5 — Plotting That Reveals Chemistry
- YouTube: _(add link when published)_
