# 4.2 — UV–Vis: Building Your First Calibration Curve

**Title:** *Turning Signal Into Concentration: Calibration, Detection Limits, and Honest Uncertainty*
**Track:** 4 — Spectroscopy · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Foundation

## Learning objective

Fit a calibration line, use it to predict the concentration of an unknown, and
report that result *honestly* — with a confidence interval, a detection limit,
and a check that a straight line was the right model in the first place. The
lesson is deliberately **not** "how to call `numpy.polyfit`." It builds the
reasoning around a calibration: what the slope and intercept mean physically, why
a residual plot beats R² for judging a fit, how uncertainty propagates into a
predicted concentration, where LOD and LOQ come from, and how a curved response
can hide behind a beautiful R² and produce confident, wrong answers. Because
every spectrum comes from `uvvis.simulate()`, the *true* concentration behind
each measurement is known, so every fit, prediction, and detection limit is
graded against the right answer.

## Why it matters

The calibration curve is the single most common quantitative task in an
analytical lab, and it is quietly full of ways to fool yourself. A straight-line
fit always returns a slope and intercept, and R² is almost always high — so the
number *looks* trustworthy whether or not it is. This notebook makes the failure
modes concrete and measurable: the well-behaved calibration recovers the true
sensitivity (slope ≈ 1.0) and predicts a blind unknown to within a fraction of a
percent *with* a real 95% interval; the blank's noise sets a detection floor
(LOD ≈ 3.3σ/slope, LOQ ≈ 10σ/slope) that differs depending on how you estimate
the noise; and a 0.3 % stray-light curvature posts R² = 0.994 — a number you'd
happily report — while its residual plot traces an unmistakable arch and
extrapolation past the linear range recovers only ~89 % of a high sample. The
throughline: a concentration without an uncertainty, a range, and a residual
check is only half a result.

## What the notebook covers

1. **What a calibration curve means** — Beer–Lambert as the reason signal scales
   with concentration, and slope (sensitivity) and intercept (zero-signal) as the
   two numbers a calibration actually measures.
2. **A realistic calibration series** — six known concentrations, three
   replicates each, plus blanks, all from fixed seeds; the standard spectra grow
   visibly with concentration.
3. **From a spectrum to one number** — peak height vs. peak area (reusing the
   3.5 local-linear-baseline measurement), both linear in concentration.
4. **Fitting the line** — least squares on all replicate points; slope, intercept
   with standard errors, R², and the residual standard deviation `s_y/x`; the
   recovered slope matches the true sensitivity.
5. **Residual plots** — the *good* fit's residuals are structureless scatter,
   establishing what "no pattern" looks like before the broken case appears.
6. **Predicting an unknown with uncertainty** — inverse prediction
   `c = (signal − b)/m` plus the Miller–Miller confidence interval; a secret
   `0.55` unknown is recovered at 100.2 % and the true value lands inside the CI.
7. **LOD and LOQ** — blank noise σ from 20 blanks; LOD = 3.3σ/slope and
   LOQ = 10σ/slope by both the blank-standard-deviation and the regression-
   residual routes, and what "below LOD / below LOQ" actually licenses you to say.
8. **When calibration fails** — injected stray-light nonlinearity gives R² = 0.994
   yet a clearly curved residual plot; restricting to the linear range restores
   R² = 0.9999 with flat residuals, and extrapolating beyond it under-predicts
   (89 % recovery at c = 2.5) — confident and wrong.
9. **A reusable `calibrate()` / `predict_concentration()` helper** — fits the
   line, reports the statistics, sets LOD/LOQ, and returns predictions with
   intervals; demonstrated on a blind unknown and graded against ground truth.

Closes with **Key Takeaways**, a **Practical Checklist**, **Common Mistakes**,
**Reporting Guidance**, and the **Next Lesson** pointer.

## Prerequisites

- 4.1 (Beer–Lambert and the Absorbance Mindset) — the linear absorbance–
  concentration relationship this lesson measures and inverts.
- 3.5 (Peak Integration and Quantitation) — the local-linear baseline + height/
  area measurement is reused to collapse each spectrum to one number. Helpful but
  not required; the notebook re-imports what it needs.
- 2.5 (Plotting That Reveals Chemistry) — helpful but not required.

## How to run

First-time setup lives in the [root README](../../../README.md#setup): create
and activate a `.venv`, then run `python -m pip install -e ".[notebooks]"`. When
the notebook opens, select the `.venv` kernel — and **restart the kernel if you
just installed the package** (see [Troubleshooting](../../../README.md#troubleshooting)).

This pulls in SciPy (for the Student-*t* confidence intervals). Then open and run
this notebook from this folder, top to bottom. It needs no external data — every
spectrum is generated from a fixed seed, so your figures and printed numbers
match the committed output. The `exports/` folder it creates (PNG figures) is
regenerable scratch and is git-ignored.

## Data

Simulated UV-Vis spectra via `from simulated_data import uvvis`. A single analyte
band (520 nm, FWHM 40, unit-concentration height 1.0 AU) on a small instrumental
offset with realistic noise drives the whole lesson: six standards × three
replicates build the calibration, twenty blanks set the detection floor, and
blind unknowns at known concentrations (0.55, 0.37) close the loop. The
nonlinearity section injects a documented stray-light deviation
(`A_obs = −log10[(1−s)·10^(−A) + s]`, s = 0.3 %) by hand, since the simulator is a
faithful *linear* Beer–Lambert model. The known concentrations are the answer
key. No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 4.2
- Previous: 4.1 — Beer–Lambert and the Absorbance Mindset *(planned)*
- Follow-up: 4.3 — NIR Preprocessing: SNV, MSC, and Scatter Correction *(planned)*
