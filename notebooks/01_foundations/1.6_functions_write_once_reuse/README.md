# 1.6 — Functions: Writing a Step Once and Reusing It

**Title:** *Functions: Writing a Step Once and Reusing It*
**Track:** 1 — Foundations · **Difficulty:** Beginner · **Length:** 12–15 min · **Type:** Onboarding

## Learning objective

Turn a repeated analysis step into a reusable method you can apply consistently: define
a function with a clear input, output, default, and description, then reuse it across a
batch by combining it with a loop.

## Why it matters

A method should be defined once and applied identically everywhere. Functions are how
you make a step portable and consistent — one definition, one place to fix, the same
behavior on every sample. This is the bridge to the reusable preprocessing steps in
Track 2 and beyond.

## What the notebook covers

1. The cost of copy-pasting a calculation across samples.
2. Wrapping Beer–Lambert in `absorbance_to_concentration(...)` with a default path length.
3. A second function for the spec check, applied with a loop across a batch.
4. Why one definition in one place is what makes a method defensible.

## Prerequisites

- 1.5 (Loops and Conditionals for Batch Thinking).

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run this notebook top to bottom. It needs no external data.

## Data

Inline toy data only — a short list of sample IDs and absorbances typed into the
notebook. No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 1.6
- Follow-up: 2.1 — NumPy Arrays: Math on Whole Spectra at Once (Track 2)
- YouTube: _(add link when published)_
