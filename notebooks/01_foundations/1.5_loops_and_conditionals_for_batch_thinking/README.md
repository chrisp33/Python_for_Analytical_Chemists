# 1.5 — Loops and Conditionals for Batch Thinking

**Title:** *Loops and Conditionals for Batch Thinking*
**Track:** 1 — Foundations · **Difficulty:** Beginner · **Length:** 12–15 min · **Type:** Onboarding

## Learning objective

Process multiple samples the same way and flag values that need attention: apply one
calculation to every sample with a `for` loop, classify results against spec limits
with `if`/`elif`/`else`, and collect the outcomes into a scannable table.

## Why it matters

Labs rarely measure one sample. The moment you have a tray of 96, you need to do the
same thing to each one without copy-paste — and you want the computer to flag the
samples that fall outside spec so your attention goes where it's needed.

## What the notebook covers

1. A `for` loop applying Beer–Lambert to a batch of samples.
2. `if`/`elif`/`else` to label each result low / pass / high against spec limits.
3. Counting out-of-spec samples and assembling a small pandas results table.

## Prerequisites

- 1.4 (Lists, Arrays, and a First Spectrum).

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run this notebook top to bottom. It needs no external data.

## Data

Inline toy data only — a short list of sample IDs and blank-corrected absorbances typed
into the notebook. No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 1.5
- Follow-up: 1.6 — Functions: Writing a Step Once and Reusing It
- YouTube: _(add link when published)_
