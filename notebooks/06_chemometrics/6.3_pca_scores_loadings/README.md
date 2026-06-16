# 6.3 — PCA I: Scores, Loadings, and Seeing Structure

**Title:** *What Your PCA Loadings Are Really Telling You About the Molecule*
**Track:** 6 — Chemometrics · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Authority Builder

## Learning objective

Understand Principal Component Analysis as a chemist, not just a coder: build it
from scratch with the SVD, read a **scores** plot to see which samples group, and
— the heart of the lesson — **read a loading as a spectrum** and map its peaks
back to real chemical bands. The notebook is deliberately not "call `PCA()` and
plot the scores." It treats the loadings as the payoff and teaches the explicit
recipe for interpreting them (peak position = which channel matters, sign = which
samples score high, opposite signs = a chemical trade-off). Because the data is
simulated, the **true pure-component spectra** and **true concentrations** are
known, so the scores are graded against concentration and the loadings against
the component spectra rather than eyeballed.

## Why it matters

PCA is the gateway to all of chemometrics and machine learning on spectra, and
the single most common way it is misused is to stop at a pretty scores scatter
without ever asking what the components *mean*. This notebook makes the chemistry
explicit and provable. On a 60-sample, three-component mixture set it recovers
exactly **three** components from the scree (99.4 % of variance in PC1–PC3, then
a cliff), shows the three classes separating **unsupervised** in the scores, and
demonstrates that the first three scores reconstruct each true concentration with
a **multiple R of 1.00**. It then proves the loadings *are* chemistry: each
loading is explained by the known component bands with **R² ≈ 1.0**, PC1 reading
as a clean **B-versus-A contrast** and PC2 as the **C axis**. Finally — using the
**scatter-dominated NIR set from 4.3** for curriculum continuity — it shows the
indispensable caveat: on raw data PC1 correlates **1.00 with scatter** and only
0.31 with the property; after SNV, PC1 correlates **1.00 with the property**.
Same algorithm, opposite meaning. The throughline: PCA finds variance, and
loadings become molecular information only once the nuisance variation is gone.

## What the notebook covers

1. **Why multivariate** — spectra are redundant; a few components drive hundreds
   of correlated channels.
2. **A three-component dataset with known chemistry** — 60 mixtures of pure
   components A/B/C in three enriched classes, with concentrations and pure
   spectra kept as ground truth.
3. **The raw data** — class overlay plus a channel-correlation heatmap that makes
   the redundancy visible.
4. **Mean-centering** — why PCA models deviations about the mean (scaling deferred
   to 6.2).
5. **PCA from scratch via the SVD** — scores `= UΣ`, loadings `= Vᵀ`, variance
   `= σ²/Σσ²`; no scikit-learn.
6. **The scree plot** — reading the elbow to recover three components.
7. **The scores plot** — unsupervised class separation, graded against true
   concentration (multiple R ≈ 1.0).
8. **Reading a loading as a spectrum** — the deep section: the three-rule recipe,
   the three loadings annotated against the component bands, an annotated PC1
   close-up, and an R²-in-component-span confirmation that loadings are pure
   chemistry.
9. **Reconstruction and compression** — error vs `k` collapses at three
   components, confirming dimensionality.
10. **The caution** — the 4.3 scatter-dominated NIR set: PC1 is scatter on raw
    data, and becomes the property only after SNV.
11. **A reusable `pca_svd()` / `pca_report()` helper** for later lessons.

Closes with **Key Takeaways**, a **Practical Checklist**, **Common Mistakes**,
**Reporting Guidance**, and the **Next Lesson** pointer.

## Prerequisites

- 4.3 (NIR Preprocessing: SNV, MSC, and Scatter Correction) — the scatter set and
  SNV are reused in the caution section. Helpful but not required; the notebook
  rebuilds what it needs.
- 6.2 (Mean-Centering, Scaling, and Why Order Matters) — referenced for the
  scaling decision; mean-centering is done inline here.
- No prior PCA needed: it is built from scratch with NumPy's SVD.

## How to run

From the repository root, once:

```bash
pip install -e ".[notebooks]"
```

Then open and run this notebook from this folder, top to bottom. It needs no
external data — every spectrum is generated from a fixed seed (`SEED = 0`), so
your figures and printed numbers match the committed output. PCA uses NumPy's SVD;
no scikit-learn is required. The `exports/` folder it creates (PNG figures) is
regenerable scratch and is git-ignored.

## Data

Two simulated sets, both with ground truth. The **primary** set is built in-notebook
from the shared `simulated_data.core` primitives: three pure-component spectra
(`add_peaks`) mixed at known, partly class-structured concentrations on a
600–1800 cm⁻¹ axis, plus detector noise — the pure spectra and concentration
matrix are the answer key. The **caution** set is a 4.3-style NIR set via
`from simulated_data import nir`, where one diagnostic analyte band encodes a
property and every sample carries its own physical scatter. No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 6.3
- Related: [4.3 — NIR Preprocessing: SNV, MSC, and Scatter Correction](../../04_spectroscopy/4.3_nir_snv_msc_scatter_correction/) (reused in the caution section); [4.5 — Raman: Cosmic Ray Removal and Fluorescence Baselines](../../04_spectroscopy/4.5_raman_cosmic_ray_fluorescence/) (cleaned spectra feed PCA)
- Follow-up: 6.4 — PCA II: Outlier Detection and Diagnostics *(planned)*; then 6.5 — PLS Regression
