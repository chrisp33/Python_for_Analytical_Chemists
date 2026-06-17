# 1.4 — Lists, Arrays, and a First Spectrum

**Title:** *Lists, Arrays, and a First Spectrum*
**Track:** 1 — Foundations · **Difficulty:** Beginner · **Length:** 12–14 min · **Type:** Onboarding

## Learning objective

Represent a simple spectrum as paired x/y data and plot it: hold a wavelength axis and
an absorbance axis as aligned sequences, do whole-spectrum math with a NumPy array, and
read a peak position back off the result.

## Why it matters

Every spectrum and chromatogram is structurally just two aligned columns — an x-axis
you set and a y-axis you measure. Once you can hold those two columns in Python and
plot one against the other, you can look at any spectrum you'll record.

## What the notebook covers

1. Aligned x/y lists and the `len(x) == len(y)` alignment check.
2. Why arrays: subtracting a baseline from a whole spectrum in one line.
3. Building a believable Gaussian absorbance band on a baseline (seeded noise).
4. Plotting absorbance vs wavelength with labelled axes; `argmax` for λ-max.

## Prerequisites

- 1.3 (Variables, Numbers, and Units).

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run this notebook top to bottom. It produces one small figure and needs no
external data.

## Data

Inline toy data only — short x/y lists plus a Gaussian band generated with `numpy`
(fixed seed). No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 1.4
- Follow-up: 1.5 — Loops and Conditionals for Batch Thinking
- YouTube: _(add link when published)_
