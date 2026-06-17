# 1.1 — Why Python Belongs on the Lab Bench

**Title:** *Why Python Belongs on the Lab Bench*
**Track:** 1 — Foundations · **Difficulty:** Beginner · **Length:** 10–12 min · **Type:** Onboarding

## Learning objective

Open a notebook, run code, and produce a simple scientific result from measurement
data — a reported mean and %RSD from replicate readings, and a concentration from an
absorbance via Beer–Lambert.

## Why it matters

Vendor software is built for one screen and one result; the moment you want the same
calculation applied to many samples, checked, or handed to a colleague who can re-run
it, you've outgrown the menus. Python is the transparent, reproducible alternative —
and a chemist can get a useful result from it on day one, without "learning to
program."

## What the notebook covers

1. Running cells and reading a printed result.
2. Mean and %RSD of replicate absorbance readings with `numpy`.
3. Absorbance → concentration with Beer–Lambert (`c = A / (ε·b)`).
4. A small plot of the replicates with the mean drawn through them.

## Prerequisites

- None. This is the first lesson.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. When the
notebook opens, select the `.venv` kernel — and **restart the kernel if you just
installed the package** (see [Troubleshooting](../../../README.md#troubleshooting)).

Open and run this notebook top to bottom. It needs no external data.

## Data

Inline toy data only — five replicate absorbance readings typed into the notebook. No
external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 1.1
- Follow-up: 1.2 — Notebooks, Scripts, and How to Not Lose Your Work
- YouTube: _(add link when published)_
