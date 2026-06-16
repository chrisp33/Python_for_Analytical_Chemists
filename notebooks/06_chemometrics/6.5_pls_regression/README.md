# 6.5 — PLS Regression: Quantitative Prediction from Spectra

**Title:** *From Seeing to Predicting: PLS Regression, Latent Variables, and Honest Error*
**Track:** 6 — Chemometrics · **Difficulty:** Intermediate · **Length:** 18–20 min · **Type:** Authority Builder

## Learning objective

Move from describing spectra (PCA, 6.3) and screening them (6.4) to **predicting a
property** from them. Understand why PCA's variance-ranked components are not what
prediction needs, what **latent variables** are (directions of maximum covariance
with the target), build **PLS regression from scratch** with the NIPALS algorithm,
choose the number of latent variables by **cross-validation**, recognise
**overfitting** by watching training error diverge from cross-validated error, and
**interpret the regression vector** as analyte chemistry. Every prediction is
graded against known concentrations on an independent test set, and the model's
regression vector is checked against the true analyte spectrum.

## Why it matters

Quantitative spectroscopy lives on the question "how much analyte is in this
sample?", and PLS is its standard answer — but it is also where two costly
mistakes hide: choosing model complexity from the training fit, and letting
information leak across a cross-validation split. This notebook makes both visible
and gradeable. On a deliberately realistic problem — a modest analyte measured
against two interferents that swing far wider and so **dominate the variance** —
PCA puts the analyte in **PC3 (just 2 % of variance)**, so principal-component
regression with the "high-variance" components is nearly blind (RMSEP 0.24 at two
components) while PLS, aimed at the property, already predicts well (RMSEP 0.089 at
two). Cross-validation then selects **three latent variables**, and the
calibration-vs-CV-vs-test error curves show the textbook overfitting fork:
training error falls to ~0.0001 with more components while CV/test error turn back
up. The final 3-LV model predicts the held-out test set with **R² = 0.994, RMSEP =
0.0176, bias = −0.003**, and its regression vector correlates **0.98 with the true
analyte spectrum** while suppressing the interferents (≈ −0.10) — proof that it
predicts from the right chemistry, not a lucky correlation. The throughline: PLS
aims at the property, and only honest validation tells you how many latent
variables to trust.

## What the notebook covers

1. **A dataset with a known property** — mixtures of a target analyte and two
   larger interferents; calibration and independent test sets; `y` known.
2. **Why PCA isn't enough** — the analyte hides in a tiny PC; PCR on high-variance
   components misses it, and a per-component PCR-vs-PLS comparison shows PLS
   reaching low error with far fewer components.
3. **Latent variables** — covariance with the target (`w ∝ Xᵀy`) vs PCA's variance.
4. **PLS from scratch (NIPALS)** — weights → scores → loadings → deflate, collapsed
   to a regression vector; heavily commented.
5. **A first model** — predicted-vs-true on calibration and test.
6. **Choosing #LV by cross-validation** — RMSECV vs number of latent variables,
   re-fitting inside each fold (no leakage).
7. **Overfitting** — training error keeps falling while CV/test error turn up.
8. **Final test prediction** — RMSEP, R², and bias against known truth.
9. **Interpreting the regression vector** — read it as a spectrum; confirm it keys
   on the analyte bands (vs the true analyte spectrum) and suppresses interferents.
10. **A reusable PLS toolkit** — `pls_fit`, `pls_predict`, `cross_val_rmse`, and a
    one-call `build_pls` wrapper.

Closes with **Key Takeaways**, a **Practical Checklist**, **Common Mistakes**
(data leakage front and centre), **Reporting Guidance**, and the **Next Lesson**
pointer.

## Prerequisites

- 6.3 (PCA I) — latent structure and the "read the vector as a spectrum" habit;
  `pca_svd` is reused for the PCA-vs-PLS contrast.
- 6.4 (PCA II: Diagnostics and Outliers) — the calibration set should be
  outlier-screened before calibration. Helpful, not required.
- 4.3 (NIR Scatter Correction) — preprocessing context for the leakage discussion.

## How to run

From the repository root, once:

```bash
pip install -e ".[notebooks]"
```

Then open and run this notebook from this folder, top to bottom. It needs no
external data — every spectrum is generated from fixed seeds, so your figures and
printed numbers match the committed output. PLS is implemented from scratch with
NumPy (NIPALS); no scikit-learn is required. The `exports/` folder it creates (PNG
figures) is regenerable scratch and is git-ignored.

## Data

Built in-notebook from the shared `simulated_data.core` primitives, with ground
truth recorded by construction. Spectra are mixtures `y·analyte + c₁·interferent₁ +
c₂·interferent₂ + noise` on a 600–1800 cm⁻¹ axis, where `y` (the target analyte
concentration) is the property to predict and the interferent concentrations span a
much wider range so they dominate the variance. Independent calibration (60) and
test (40) sets are drawn from the same generator with different seeds. No external
datasets, and no new simulator-package code.

## Ground truth and grading

The true analyte concentration `y` is known for every calibration and test sample,
and the true pure-component spectra are known. Predictions are graded on the
held-out test set by RMSEP, R², and bias against the true `y`; the number of latent
variables is justified by the RMSECV curve and confirmed against the test error;
and the fitted regression vector is validated by its correlation with the true
analyte spectrum (and its suppression of the interferents).

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 6.5
- Previous: [6.4 — PCA II: Diagnostics and Outliers](../6.4_pca_diagnostics_and_outliers/)
- Next: 6.6 — Validation Done Right: Cross-Validation, RMSEP, and Overfitting *(planned)*; then 6.7 — Calibration Transfer
