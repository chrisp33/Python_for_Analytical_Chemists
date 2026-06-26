# 3.6 — Signal Averaging and the √N Rule: When More Scans Help and When They Don't

**Title:** *Why 1000 Scans Didn't Help: The Truth About Signal Averaging*
**Track:** 3 — Signal Processing · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Measurement-judgment (moat)

## Learning objective

Use signal averaging well: measure the √N signal-to-noise improvement under ideal
white noise, recognize the cases where averaging stops helping (drift, correlated
noise) or actively misleads (a changing sample), and decide how many scans are worth
acquiring.

## Why it matters

Co-adding scans is the most common SNR move in spectroscopy and MS, and it silently
fails when the noise isn't white or the sample isn't stable. Knowing *when* the √N
rule holds — and when more scans degrade or falsify the result — is measurement
judgment a generic coding tutorial can't teach.

## What the notebook covers

1. Defining SNR and the RMS-vs-truth metric on a single noisy band.
2. The ideal case: averaging up to 64 scans tracks the `σ₁/√N` prediction exactly.
3. Why √N — coherent signal vs incoherent noise — and the quadratic time cost.
4. Drift: a systematic creep that doesn't average out, producing an optimal N beyond
   which more scans make the result worse.
5. A changing (decaying) sample: a clean average that reports a wrong, biased band.
6. The judgment: diminishing returns, a stability budget, and when averaging is the
   wrong tool.

## Prerequisites

- 3.1 (Noise, Signal, and Why Preprocessing Exists) — the reproducibility test in
  particular; Track 1–2 foundations.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. Produces three small figures; needs no external data.

## Data

Inline generated data only — repeated noisy scans of one band, with white noise,
baseline drift, and sample decay imposed deliberately so each failure mode is exact.
No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → Track 3
- Follow-up: 3.7 — Peak Fitting with Gaussians, Lorentzians, and Voigt (planned)
- YouTube: _(add link when published)_

> **Note for maintainers:** this lesson was added as **3.6** in a focused sprint,
> shifting the planned *Peak Fitting* to 3.7 and *FFT* to 3.8. `docs/curriculum.md`
> still lists the old numbering and has no Signal Averaging lesson — it needs a human
> pass. See `docs/STATUS.md`.
