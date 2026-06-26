# 3.1 — Noise, Signal, and Why Preprocessing Exists

**Title:** *What's Actually in a Raw Spectrum (and Why You Can't Skip Preprocessing)*
**Track:** 3 — Signal Processing · **Difficulty:** Intermediate · **Length:** 14–16 min · **Type:** Foundation

## Learning objective

See why raw measurement data need preprocessing: name the nuisance components (noise,
baseline, drift, artifacts), tell signal from nuisance, and understand that
preprocessing is scientific judgment with consequences, not cosmetic cleanup.

## Why it matters

The number an instrument hands you is signal plus a pile of things you don't want.
Every later Track 3 step — smoothing, baseline correction, peak detection — exists to
separate the two. Getting that separation wrong either buries real chemistry or
fabricates some that was never there, and it flows straight into the result you report.

## What the notebook covers

1. Assembling a raw spectrum from known parts: true bands, baseline, noise, a spike.
2. What distinguishes signal (smooth, correlated, reproducible) from nuisance.
3. The reproducibility test — measure twice; what repeats is signal.
4. How an ignored baseline biases a reported band height.
5. The noise-vs-resolution trade-off of a moving average.
6. Preprocessing as judgment: choices with consequences, and why they must be recorded.

## Prerequisites

- 2.2 (Indexing, Slicing, and Selecting Spectral Regions); Track 1–2 foundations.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. Produces three small figures; needs no external data.

## Data

Inline generated data only — a two-band spectrum built from known components with
`numpy` (fixed seed), so signal and each nuisance are known exactly. No external
datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 3.1
- Follow-up: 3.2 — Savitzky–Golay Smoothing and Derivatives
- YouTube: _(add link when published)_
