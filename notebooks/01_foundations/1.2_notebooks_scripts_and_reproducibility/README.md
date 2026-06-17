# 1.2 — Notebooks, Scripts, and How to Not Lose Your Work

**Title:** *Notebooks, Scripts, and How to Not Lose Your Work*
**Track:** 1 — Foundations · **Difficulty:** Beginner · **Length:** 8–10 min · **Type:** Onboarding

## Learning objective

Keep an analysis organized so you can re-run it later and get the same answer:
understand cell execution order, use Restart & Run All as a reproducibility test, and
know when to reach for a script instead.

## Why it matters

A result you can't reproduce isn't a result yet — it's a number you got once.
Reproducibility starts with being able to re-run an analysis and get the identical
value. A notebook makes that nearly free, *if* you treat it like a lab notebook.

## What the notebook covers

1. The kernel as running memory; why cells run in the order you run them.
2. The reproducibility test: same inputs → same answer, confirmed.
3. Gathering method constants (path length, blank, dilution) at the top.
4. When a notebook is the right tool and when a script is.

## Prerequisites

- 1.1 (Why Python Belongs on the Lab Bench).

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create and
activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. Select the
`.venv` kernel and restart it if you just installed the package.

Open and run this notebook top to bottom, then try **Kernel → Restart & Run All**.

## Data

Inline toy data only — a sample reading, a blank, and a dilution factor typed into the
notebook. No external datasets and no `simulated_data` package required.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 1.2
- Follow-up: 1.3 — Variables, Numbers, and Units Without Tears
- YouTube: _(add link when published)_
