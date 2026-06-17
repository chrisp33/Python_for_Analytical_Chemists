# 2.7 — Joining Measurements and Metadata

**Title:** *When the Sample Table and the Spectra Live in Different Files*
**Track:** 2 — Scientific Computing · **Difficulty:** Intermediate · **Length:** 14–16 min · **Type:** Core

## Learning objective

Reunite measurements and metadata that arrived in separate files: merge on the
sample ID, choose inner vs left joins, and catch the failures a join exposes —
missing metadata and duplicate IDs.

## Why it matters

Instrument output and sample metadata almost always live in different files. Joining
them correctly is routine — and it is exactly where mismatches surface: a sample with
no metadata, or a duplicate ID that silently multiplies your rows and corrupts a count.

## What the notebook covers

1. Merging a measurements table with a metadata table on `sample_id`.
2. Inner vs left joins; seeing missing metadata with `how="left"` and `indicator=True`.
3. How duplicate keys multiply rows, and detecting them with `.duplicated`.
4. Validating a merge with `validate="m:1"` so a bad join fails loudly.

## Prerequisites

- 2.3 (pandas DataFrames for Sample Tables); 2.6 for missing-value handling.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run top to bottom. It needs no external data.

## Data

Inline toy data only — a measurements table and a metadata table with deliberate
mismatches and a duplicate ID, typed into the notebook. No external datasets and no
`simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 2.7
- Follow-up: 2.8 — Reshaping Data for Analysis
- YouTube: _(add link when published)_

> **Note for maintainers:** this lesson's topic (Joining Measurements and Metadata)
> supersedes the older curriculum placeholder for 2.7 ("Saving Results: Arrays,
> Tables, and Figures"), which is not part of this sprint. See `docs/STATUS.md`.
