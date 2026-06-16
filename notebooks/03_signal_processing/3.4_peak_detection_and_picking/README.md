# 3.4 — Peak Detection and Picking

**Title:** *Is That a Peak? Detecting Real Bands and Rejecting Fake Ones*
**Track:** 3 — Signal Processing · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Foundation

## Learning objective

Understand what actually makes something a peak, and learn to detect real bands
while rejecting noise — choosing the four `find_peaks` parameters (**height,
prominence, distance, width**) deliberately and *grading every result against
known ground truth*. The aim is to teach peak detection as a reasoning problem,
not to call `scipy.signal.find_peaks()`.

## Why it matters

A peak is a local maximum, and a noisy spectrum has hundreds of them — so "find
the local maxima" is a noise detector, not a peak detector. In the notebook a bare
`find_peaks` returns ~85 maxima for 4 real bands. The lesson builds the intuition
that separates signal from noise: why **height** fails over a drifting baseline
(no single threshold both catches every band and rejects the noise), why
**prominence** is the robust workhorse (it measures how far a peak rises above its
*local* surroundings, so the baseline cancels out), and how **distance** and
**width** encode physics (expected resolution; spike rejection). Crucially, it
treats detection as a *measurement* with two error modes — false positives
(invented peaks) and false negatives (missed bands) — and scores them against the
simulator's known truth, then shows that detection quality is mostly a
*preprocessing* story: smoothing and baseline correction matter more than the
detector's own settings.

## What the notebook covers

1. **What even is a peak?** — on a pure-noise region, a bare detector finds
   ~138 "peaks" where there are zero. Reframes the task as *separating real
   maxima from noise*.
2. **A realistic test spectrum** — four bands (tall/isolated, a close B–C pair,
   broad) dressed in noise and a sloping baseline, with the true centres kept
   from `meta.attrs["peaks"]` as an answer key, plus a clean twin for reference.
3. **The naive detector** — `find_peaks(y)` returns ~85 detections for 4 bands.
4. **Height** — the first filter, and why it's fragile: over a drifting baseline
   no single height threshold works (low admits noise; high misses bands).
5. **Prominence** — the concept that matters most, visualized as the vertical
   drop each peak stands above its surroundings; one threshold recovers all four
   bands and nothing else.
6. **Distance** — minimum separation; too small does little, too large *merges*
   the real B–C pair (a false negative made by a parameter).
7. **Width** — rejecting injected single-point spikes (cosmic-ray–like) that
   prominence can't see, while keeping the broad real bands.
8. **All four knobs together** — ~85 maxima → exactly four real bands.
9. **Grading against ground truth** — a `grade_peaks()` helper returns true
   positives, false positives, false negatives, precision, recall; a prominence
   sweep makes the false-positive ↔ false-negative trade-off explicit.
10. **Preprocessing changes everything** — the same loose threshold drowns on raw
    data but is clean after Savitzky–Golay smoothing (3.2); a single height
    threshold becomes usable again after AsLS baseline correction (3.3).
11. **The overlapping-peak limit** — two bands under one summit give one maximum;
    the second derivative *flags* the pair (minima at 545/573), but separating
    them needs *fitting* (3.6), not detection.
12. **A reusable `detect_peaks()` helper** — sensible defaults, returns positions
    plus per-peak height/prominence/FWHM in axis units, for later notebooks.

## Prerequisites

- 3.2 (Savitzky–Golay Smoothing and Derivatives) and 3.3 (AsLS Baseline
  Correction) — both reused directly in the preprocessing section. Helpful but
  not required; the notebook re-imports what it needs.
- 2.4 / 2.5 (reading files and plotting) — helpful but not required.

## How to run

From the repository root, once:

```bash
pip install -e ".[notebooks]"
```

This pulls in SciPy (for `scipy.signal`). Then open and run this notebook from
this folder, top to bottom. It needs no external data — every spectrum is
generated from a fixed seed, so your figures match the committed output. The
`exports/` folder it creates (PNG figures) is regenerable scratch and is
git-ignored.

## Data

Simulated UV-Vis spectra via `from simulated_data import uvvis`. The main test
spectrum (`seed=11`) has four bands at 450, 550, 600, and 690 nm with a sloping
baseline and Gaussian noise; the true centres come from `meta.attrs["peaks"]` and
every detection is graded against them. A second, noise-free spectrum (`seed=3`,
bands at 545/575 nm) demonstrates the overlapping-peak limit. No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 3.4
- Previous: [3.3 — Asymmetric Least Squares (AsLS) Baseline Correction](../3.3_asls_baseline_correction/)
- Follow-up: 3.5 — Peak Integration and Quantifying Area *(planned)*
