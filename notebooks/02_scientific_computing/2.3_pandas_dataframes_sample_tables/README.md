# 2.3 — pandas DataFrames for Sample Tables

**Title:** *Keeping Every Measurement Next to Its Metadata*
**Track:** 2 — Scientific Computing · **Difficulty:** Beginner · **Length:** 15–18 min · **Type:** Core

## Learning objective

Keep measurements and their metadata together in one table, then filter rows by
condition and compute per-group summaries.

## Why it matters

Your measurements always travel with metadata — batch, operator, instrument,
concentration. Keeping signal and metadata in one row prevents the mix-ups that come
from parallel lists drifting out of sync.

## What the notebook covers

1. Building and inspecting a sample table (`shape`, `dtypes`, selection).
2. Filtering rows by one or more conditions.
3. Group summaries with `groupby(...).agg([...])` (per-batch mean/SD/count).
4. Adding a computed pass/review column with `np.where`.

## Prerequisites

- 2.2 (Indexing, Slicing, and Selecting Spectral Regions); the boolean-mask idea
  carries over from arrays to tables.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. It needs no external data.

## Data

Inline toy data only — a small worklist of sample IDs, batches, operators,
concentrations, and absorbances typed into the notebook. No external datasets and no
`simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 2.3
- Follow-up: 2.4 — Reading Real Instrument Files (CSV, TXT, and the Messy Ones)
- YouTube: _(add link when published)_
