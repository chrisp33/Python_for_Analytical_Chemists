# 3.2 — Savitzky–Golay Smoothing and Derivatives

**Title:** *Smoothing Without Lying: Savitzky–Golay and Derivatives for Spectra*
**Track:** 3 — Signal Processing · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Foundation

## Learning objective

Apply Savitzky–Golay smoothing and compute first and second derivatives
*correctly* — choosing the window length and polynomial order from measurable
properties of the spectrum (peak width, noise level, point spacing) rather than
by trial and error.

## Why it matters

Smoothing is one function call, so it feels free — and that is exactly why it
quietly ruins data. The wrong window flattens narrow peaks and biases peak
heights without anyone noticing. This notebook treats smoothing as a deliberate
trade-off between **noise** and **resolution**, and teaches the rule of thumb
that anchors every good choice: **size the window to your narrowest peak**
(window ≈ one FWHM in points). It then shows what derivatives buy you — baseline
removal and the ability to resolve overlapping bands — and the price they
charge: amplified noise.

## What the notebook covers

1. **Recap of noise & smoothing** — a short, self-contained primer (since 3.1
   isn't built yet): signal vs. noise, smoothing as local averaging, and the two
   numbers that govern everything (FWHM and point spacing).
2. **A spectrum with known peak widths** — a narrow (15 nm) and a broad (50 nm)
   band, generated noisy *and* noise-free from the same seed so every method can
   be graded against the truth. Prints points-per-FWHM.
3. **Moving average** — the simple boxcar baseline, and why it distorts peaks.
4. **Savitzky–Golay** — fitting a local polynomial instead of averaging; a
   matched-window comparison shows it keeps 98% of peak height vs. 81% for the
   boxcar.
5. **Window length vs. polynomial order** — a sweep grid making the interaction
   visible.
6. **Over- vs. under-smoothing, quantified** — residual-noise and
   height-retention curves that expose the sweet spot at window ≈ 1 FWHM.
7. **First derivative** — removes baseline offset; the zero-crossing locates the
   peak centre (recovers 499 nm for a true 500 nm band).
8. **Second derivative** — resolves two heavily overlapping bands (600 + 635 nm)
   that look like a single bump.
9. **Why derivatives amplify noise** — the same 2nd derivative, under- vs.
   adequately-smoothed, side by side.
10. **Practical rules of thumb** — a pocket reference card.
11. **A reusable `smooth()` / `derivative()` helper** — sane, peak-width-aware
    defaults for later notebooks.

## Prerequisites

- 3.1 (Noise, Signal, and What Smoothing Really Does) — *not yet built*; the key
  ideas are recapped inline in Section 1.
- 2.4 / 2.5 (reading files and plotting) — helpful but not required.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create
and activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. When
the notebook opens, select the `.venv` kernel — and **restart the kernel if you
just installed the package** (see [Troubleshooting](../../../README.md#troubleshooting)).

This also pulls in SciPy (for `savgol_filter`). Then open and run this notebook
from this folder, top to bottom. It needs no external data — every spectrum is
generated from fixed random seeds, so your figures match the committed output.
The `exports/` folder it creates (PNG figures) is regenerable scratch and is
git-ignored.

## Data

Simulated UV-Vis spectra via `from simulated_data import uvvis`: one two-band
test spectrum with known FWHMs (`seed=11`, a 15 nm and a 50 nm band) used noisy
and noise-free, and a heavily-overlapping pair (`seed=3`, bands at 600 and
635 nm) for the derivative sections. No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 3.2
- Previous: 3.1 — Noise, Signal, and What Smoothing Really Does *(planned)*
- Follow-up: 3.3 — Baseline Correction Fundamentals
- YouTube: _(add link when published)_
