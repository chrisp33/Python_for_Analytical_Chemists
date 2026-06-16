# 3.3 — Asymmetric Least Squares (AsLS) Baseline Correction

**Title:** *The Baseline Lie: Why Your Peaks Aren't Where You Think (and How AsLS Fixes It)*
**Track:** 3 — Signal Processing · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Foundation

## Learning objective

Understand what a baseline is, *prove* how it distorts both interpretation and
quantitation, and correct it with Asymmetric Least Squares — choosing the two
parameters (**λ** smoothness, **p** asymmetry) deliberately and verifying the
result against measurable, ground-truth-free criteria. The aim is to *teach
baseline correction*, not just call a function.

## Why it matters

Baseline correction looks like one line of code, so it gets applied
thoughtlessly — and a careless correction does as much damage as none. A
background that lifts a spectrum off zero doesn't just look different: it inflates
peak heights and areas and **changes the ratio between bands**, which is the
number scientists use to infer relative concentration. In the notebook's example
a true height ratio of ~2.0 collapses to ~1.2 under a sloping baseline, and the
*area* ratio flips outright (the smaller band appears larger). The lesson treats
correction as a real measurement decision: it builds AsLS from scratch, shows
exactly what λ and p do, names the signatures of under- and over-correction, and
gives a checklist for judging whether a correction is scientifically honest.

## What the notebook covers

1. **The problem, before any algorithm** — one clean spectrum, then the *same*
   chemistry with a sloping and a curved baseline. Because the simulator's
   baseline is additive and concentration-independent, the *true baseline* is
   recovered exactly by differencing noise-free twins — the answer key.
2. **What a baseline is** — the slow-vs-sharp contrast that every method exploits,
   and where baselines come from (lamp drift, scattering, fluorescence, matrix).
3. **Why it distorts the science (measured)** — peak height, area, and band ratio
   on all three spectra; the ratio (apparent chemistry) shifts by tens of percent.
4. **The idea behind AsLS** — smoothness (penalize curvature, λ) plus asymmetry
   (weight points above the baseline weakly, p).
5. **AsLS from scratch** — ~20 commented lines: second-difference penalty,
   iteratively reweighted penalized least squares. No black box.
6. **Applying it** — estimated vs. true baseline, corrected vs. clean truth, with
   baseline RMSE (~0.02–0.03 AU) against the answer key.
7. **λ — the smoothness knob** — a sweep showing the U-shaped error (too small
   chases peaks; too large is too stiff; sweet spot ≈ 1e6).
8. **p — the asymmetry knob** — a sweep showing p≈0.5 slicing through peaks vs.
   small p hugging the valleys, tracked by the most-negative corrected value.
9. **Under- vs. over-correction** — the two failure modes side by side, each with
   its visual signature (residual bow vs. negative scoop).
10. **Judging a correction scientifically** — an `evaluate_correction()` helper:
    signal-free regions ≈ 0, no negative dips into peaks, height/ratio recovery.
    Three of the four tests need **no** ground truth, so they transfer to real data.
11. **A reusable `baseline_correct()` helper** — returns corrected signal +
    baseline with sensible defaults, for later notebooks.

## Prerequisites

- 3.2 (Savitzky–Golay Smoothing and Derivatives) — derivatives *sidestep*
  baselines; this lesson *removes* them. Helpful but not required.
- 2.4 / 2.5 (reading files and plotting) — helpful but not required.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create
and activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. When
the notebook opens, select the `.venv` kernel — and **restart the kernel if you
just installed the package** (see [Troubleshooting](../../../README.md#troubleshooting)).

This also pulls in SciPy (for `scipy.sparse` / `spsolve`). Then open and run this
notebook from this folder, top to bottom. It needs no external data — every
spectrum is generated from a fixed seed, so your figures match the committed
output. The `exports/` folder it creates (PNG figures) is regenerable scratch and
is git-ignored.

## Data

Simulated UV-Vis spectra via `from simulated_data import uvvis`: one two-band
test spectrum (`seed=7`, bands at 450 nm and 600 nm) generated three ways — clean,
with a sloping baseline, and with a curved baseline — each paired with a
noise-free twin so the true baseline is known exactly. No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 3.3
- Previous: [3.2 — Savitzky–Golay Smoothing and Derivatives](../3.2_savgol_smoothing_derivatives/)
- Follow-up: [3.4 — Peak Detection and Picking](../3.4_peak_detection_and_picking/)
- YouTube: _(add link when published)_
