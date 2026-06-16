# 2.5 — Plotting That Reveals Chemistry

**Title:** *Spectral Plots That Actually Show the Chemistry*
**Track:** 2 — Scientific Computing · **Difficulty:** Intermediate · **Length:** 15–18 min · **Type:** Foundation

## Learning objective

Move beyond the default `matplotlib` plot and build figures that communicate
chemical information: labelled axes with units, overlays that expose sample
differences, meaningful colour, shaded regions of interest, annotations that
name features, publication-quality formatting — and the discipline to avoid
misleading visualizations.

## Why it matters

A good plot is an analytical instrument. The default `plt.plot` answers "what
does the data look like?"; your real questions are chemical — is the analyte
growing with concentration, did this batch pick up a contaminant, is that bump
real or noise? The same skills that *reveal* chemistry can also *fabricate* it
(a truncated axis, a rainbow colormap, an unfair overlay), so honesty is treated
as a design constraint, not a style preference. This notebook is **not** a
matplotlib tutorial — matplotlib is the pen; the subject is communication.

## What the notebook covers

Each section pairs a *default plot* with a *revised plot* and the chemical
question it now answers.

1. **Axis labels, units, and direction** — pulled from the `Dataset` so they
   never drift; the IR/Raman reversed-axis convention.
2. **Colour with meaning** — sequential colormaps + colourbar for ordered
   quantities (concentration), the colourblind-safe Okabe-Ito palette for
   categories; why to avoid `jet`/rainbow and red/green.
3. **Overlays** — exposing a contaminant band that a single spectrum hides; the
   "only overlay comparable spectra" rule.
4. **Highlighting regions of interest** — `axvspan` integration windows and a
   contaminant-watch region.
5. **Annotations** — labelling λmax (computed from the data) and the contaminant.
6. **Publication-quality formatting** — an `rcParams` style block; export to
   300-dpi PNG and vector SVG.
7. **Avoiding misleading visualizations** — honest-vs-misleading on identical
   data: truncated y-axis, `jet` colormap, differently-processed overlays.
8. **A reusable `plot_spectra()` helper** — the plotting vocabulary later
   notebooks reuse.

## Prerequisites

- 2.2, 2.3 (NumPy arrays and pandas DataFrames) — briefly inlined.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create
and activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. When
the notebook opens, select the `.venv` kernel — and **restart the kernel if you
just installed the package** (see [Troubleshooting](../../../README.md#troubleshooting)).

Open and run this notebook from this folder (top to bottom). It needs no
external data — every spectrum is generated from fixed random seeds, so your
figures match the committed output exactly. The `exports/` folder it creates
(300-dpi PNG + SVG) is regenerable scratch and is git-ignored.

## Data

Simulated UV-Vis spectra via `from simulated_data import uvvis`: one clean
spectrum (`seed=7`), a five-point Beer–Lambert concentration series (`seed=3`),
and three "batches" (`seed=11/12/13`) where one carries a contaminant band near
520 nm. No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 2.5
- Previous: 2.4 — Reading Real Instrument Files
- Follow-up: 2.6 — Tidy Data and Reshaping Spectral Matrices
- YouTube: _(add link when published)_
