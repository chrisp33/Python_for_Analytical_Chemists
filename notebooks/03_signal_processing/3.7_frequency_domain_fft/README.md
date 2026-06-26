# 3.7 — Frequency Domain: A Practical Look at the FFT

**Title:** *Hidden Rhythms: What the FFT Actually Tells an Analytical Chemist*
**Track:** 3 — Signal Processing · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Measurement-science

## Learning objective

Read a signal in both the time and frequency domains, use the FFT to find periodic
interference hiding under noise (a pump, mains hum, a daily cycle), and recognize the
two traps that make an FFT mislead you: aliasing and spectral leakage.

## Why it matters

Pumps pulse, mains electricity hums, air handling cycles through the day — periodic
interferences ride on your signal as a faint ripple that's invisible in the time
trace. The FFT concentrates each repeating component into a sharp peak whose frequency
fingerprints its source, turning vague wobble into a diagnosable cause.

## What the notebook covers

1. Building a signal with two sinusoids (5 Hz pump, 50 Hz mains) plus noise.
2. The time-domain view, and why frequencies can't be read off it.
3. Computing the FFT (`np.fft.rfft`) to reveal the hidden frequencies as peaks.
4. Frequency and period as physics, and mapping a peak to its physical source.
5. Aliasing: how undersampling puts a peak at a false frequency (the Nyquist rule).
6. Spectral leakage and windowing (Hann) to suppress it.
7. Lab applications: instrument oscillations, pumps, periodic contamination, and
   daily rhythms in sensor data.
8. Reading an FFT as interpretation and measurement judgment, not arithmetic.

## Prerequisites

- 3.1 (Noise, Signal, and Why Preprocessing Exists); Track 1–2 foundations.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. Produces five small figures; needs no external data.

## Data

Inline generated data only — sinusoids, an undersampled tone, a leaky tone, and a
multi-day sensor log, all built with `numpy` (fixed seed). No external datasets and no
`simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → Track 3 (FFT)
- Follow-up: 4.1 — Beer–Lambert and the Absorbance Mindset (Track 4)
- YouTube: _(add link when published)_

> **Note for maintainers:** placed at **3.7** per instruction. This shifts the planned
> *Peak Fitting* lesson to **3.8**. `docs/curriculum.md` still lists the original Track 3
> numbering (Peak Fitting 3.6, FFT 3.7, no Signal Averaging) — it needs a human pass.
> See `docs/STATUS.md`.
