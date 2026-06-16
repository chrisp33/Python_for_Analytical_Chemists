# 6.4 — PCA II: Diagnostics and Outliers

**Title:** *Can You Trust That Sample? T², Q, and the Two Ways to Be an Outlier*
**Track:** 6 — Chemometrics · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Authority Builder

## Learning objective

Turn the PCA model from 6.3 into a diagnostic instrument. Learn the two
independent distances every sample has from a PCA model — **Hotelling's T²**
(distance *within* the model) and **Q residual / SPE** (distance *to* the model) —
build both from scratch with their control limits, combine them in the
**influence plot**, and use **leverage** and the **residual spectrum** to decide
what each outlier means. The defining lesson is **score-distance vs
residual-distance thinking**, and the judgment that follows: an outlier is not
automatically bad data — a high-T² sample is often a valid extreme worth keeping,
while a high-Q sample is an unmodelled feature to investigate.

## Why it matters

A scores plot shows clusters but never says which samples to trust, and the most
expensive chemometrics mistakes come from either deleting good extremes or
keeping broken measurements. This notebook makes the distinction objective and
provable. Fitting a three-component PCA model on 60 clean samples, it sets 99 %
control limits (T² = 12.9 via the F-distribution, Q = 0.057 via
Jackson–Mudholkar) with **zero** calibration exceedances, then screens a fresh
batch containing three kinds of **planted** outlier: a genuine high-concentration
**extreme**, an **unmodelled contaminant** band, and a **cosmic-ray spike**. All
seven planted outliers are caught (precision and recall = **1.00**, no false
alarms) and each lands in the predicted quadrant — the extreme breaches **T²
only** (T² = 16.7, Q below limit: it still fits the chemistry), while the
contaminant and spike breach **Q only** (the spike's Q is ~1000× a normal
sample's). The residual spectra then show *why* each high-Q sample fails — a clean
band at 1000 cm⁻¹ for the contaminant, a single pixel for the spike — turning Q
from a flag into a diagnosis. The throughline: **not every outlier is bad data**,
and T² vs Q is what tells them apart.

## What the notebook covers

1. **Recap the 6.3 model** — rebuild the three-component set, fit PCA, keep three
   components as the reference definition of "normal."
2. **Reconstruction error revisited** — the per-sample residual is the seed of Q.
3. **Two kinds of "far"** — a 2D cartoon separating distance *within* the model
   (T²) from distance *to* the model (Q).
4. **Hotelling's T²** — variance-scaled score distance, with the F-distribution
   control limit.
5. **Q residuals (SPE)** — residual size, with the Jackson–Mudholkar limit.
6. **The influence plot** — T² vs Q and its four quadrants; clean set in control.
7. **Planted outliers** — screen a fresh batch (extreme / contaminant / spike)
   against the fixed model and grade detection against the known labels.
8. **Why not all outliers are bad data** — residual spectra diagnose the cause and
   drive the keep-vs-investigate-vs-discard decision.
9. **Leverage** — which calibration samples steer the model, and why screening
   precedes calibration.
10. **A reusable `pca_diagnostics()` helper** for 6.5 and 6.6.

Closes with **Key Takeaways**, a **Practical Checklist**, **Common Mistakes**,
**Reporting Guidance**, and the **Next Lesson** pointer.

## Prerequisites

- 6.3 (PCA I: Scores, Loadings, and Seeing Structure) — reuses its `pca_svd`
  helper, dataset, scores/loadings, and reconstruction error. Required reading.
- 4.5 (Raman: Cosmic Ray Removal) — the `add_cosmic_rays` artifact is reused to
  manufacture the "bad measurement" outlier. Helpful, not required.

## How to run

From the repository root, once:

```bash
pip install -e ".[notebooks]"
```

Then open and run this notebook from this folder, top to bottom. It needs no
external data — every spectrum is generated from fixed seeds, so your figures and
printed numbers match the committed output. T²/Q control limits use
`scipy.stats`; PCA is the from-scratch SVD from 6.3. The `exports/` folder it
creates (PNG figures) is regenerable scratch and is git-ignored.

## Data

Built in-notebook from the shared `simulated_data` primitives, with ground truth
recorded by construction. The **calibration** set is the 6.3 three-component
mixture set (`build_axis` + `add_peaks`, known concentrations). The **screening
batch** adds outliers whose type is known: a high-concentration extreme, ordinary
mixtures plus an unmodelled contaminant band at 1000 cm⁻¹, and ordinary mixtures
plus a cosmic-ray spike (`core.artifacts.add_cosmic_rays`). No external datasets,
and no new simulator-package code.

## Ground truth and grading

The label and type of every batch sample are known, as are all concentrations and
the noise-free spectra. Detection is graded as precision/recall of the combined
T²/Q flags against the planted-outlier rows, and each outlier's **quadrant**
(high-T² vs high-Q) is checked against its expected type — verifying that the
valid extreme is high-T²/low-Q while the contaminant and spike are high-Q.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 6.4
- Previous: [6.3 — PCA I: Scores, Loadings, and Seeing Structure](../6.3_pca_scores_loadings/)
- Next: 6.5 — PLS Regression: Quantitative Prediction from Spectra *(planned)*;
  the T²/Q screen is the quality gate before calibration
