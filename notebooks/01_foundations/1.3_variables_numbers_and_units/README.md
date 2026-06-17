# 1.3 — Variables, Numbers, and Units Without Tears

**Title:** *Variables, Numbers, and Units Without Tears*
**Track:** 1 — Foundations · **Difficulty:** Beginner · **Length:** 10–12 min · **Type:** Onboarding

## Learning objective

Track measured values and their units clearly enough to avoid silent unit mistakes:
store quantities in unit-tagged variables, convert in explicit steps, and report with
units and sensible precision.

## Why it matters

Most wrong results in a lab are unit slips, not measurement errors — a milligram read
as a gram, a millilitre treated as a litre. Python can't know your units, but naming
and converting them explicitly makes a wrong answer *look* wrong on the page.

## What the notebook covers

1. Unit-tagged variable names (`mass_mg`, `volume_L`) for a standard prep.
2. Dilution and molarity with explicit `mg → g` and `mL → L` conversions.
3. The classic silent unit error (a missing `mL → L`) — a factor-of-1000, no error raised.
4. Integers vs floats, and formatting reported numbers with units.

## Prerequisites

- 1.2 (Notebooks, Scripts, and Reproducibility).

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run this notebook top to bottom. It needs no external data.

## Data

Inline toy data only — a weighed mass, a molar mass, and a flask volume typed into the
notebook. No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 1.3
- Follow-up: 1.4 — Lists, Arrays, and a First Spectrum
- YouTube: _(add link when published)_
