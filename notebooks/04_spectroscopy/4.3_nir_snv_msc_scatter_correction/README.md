# 4.3 — NIR Preprocessing: SNV, MSC, and Scatter Correction

**Title:** *NIR Looks Like Spaghetti — SNV and MSC Untangle It*
**Track:** 4 — Spectroscopy · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Foundation

## Learning objective

Understand *why* near-infrared spectra are dominated by physical scatter, correct
that scatter with SNV and MSC built from scratch, and — most importantly — decide
**whether you should**. The lesson is deliberately not "call `snv()` and move on."
It treats scatter correction as what it really is: an **assumption about the
data**. SNV and MSC each declare the per-sample level and scale to be *nuisance*
and remove them; that is a gift when the variation really is scatter and a
disaster when it is the signal. Because every spectrum comes from `nir.simulate()`,
the *true* per-sample slope and offset are known, so every correction is graded
against the right answer instead of admired.

## Why it matters

NIR is the workhorse of pharmaceutical, food, and agricultural QC, and almost no
NIR model works without preprocessing — yet preprocessing is where the silent
mistakes live. Overlay raw NIR spectra of related samples and you get spaghetti:
broad overtone bands shifted and tilted by particle size and packing, with the
chemistry buried underneath. The notebook makes both the fix and its failure mode
measurable. On a set where the property is a **band-ratio** (a shape change),
SNV and MSC lift the analyte-vs-property correlation from **0.79 to ≈ 1.00** and
move the chemistry from PC2 onto a dominant PC1 (91 % → 99 % of variance) —
exactly the readiness a downstream PCA/PLS needs. Then, on a set where the property
is an **overall level**, the *same* corrections destroy it: a raw correlation of
**0.87** collapses to **≈ 0**. The throughline, stated plainly in the notebook:
the deciding question is always *"is the variation I'm about to remove nuisance
scatter, or chemically meaningful signal?"*

## What the notebook covers

1. **Why NIR is scatter-dominated** — broad overlapping overtone/combination
   bands, diffuse reflectance, and sample presentation give the standard affine
   model `x_measured = b·x_true + a` (per-sample multiplicative slope + additive
   offset).
2. **A realistic NIR set with ground truth** — 24 samples sharing a broad matrix,
   differing in one diagnostic analyte band whose height encodes a property `y`;
   each sample carries its own true scatter slope/offset (from `meta`) and noise.
3. **The spaghetti plot** — raw overlay colored by the true property; the color
   order is scrambled because scatter, not chemistry, controls the picture.
4. **Anatomy of scatter** — one clean spectrum distorted by pure multiplicative,
   pure additive, and both, tied back to the model.
5. **SNV from scratch** — `(x − mean)/std` per spectrum; reference-free; the
   assumption that mean/std are set by scatter is named explicitly.
6. **MSC from scratch** — least-squares fit `x ≈ a + b·ref` against the mean
   spectrum, then `(x − a)/b`; reference-**dependent**, and why that matters for
   transfer.
7. **Raw vs. SNV vs. MSC** — three-panel overlay; spaghetti collapses and the
   analyte band fans out cleanly with the property.
8. **Grading against known scatter** — raw spectrum mean tracks the true offset
   (r ≈ 0.99) and spread tracks the true slope (r ≈ 0.97); analyte-band recovery
   rises from 0.79 (raw) to 0.999 (SNV/MSC).
9. **PCA / PLS readiness** — PCA from scratch (SVD); raw PC1 tracks scatter offset
   while the property hides in PC2, and after correction PC1 *is* the property.
10. **When they help** — scatter-dominated diffuse-reflectance data with
    shape/ratio chemistry headed for PCA/PLS.
11. **When they hurt (on purpose)** — a global-level dataset where SNV/MSC
    normalize the real signal away (0.87 → ≈ 0), with the lesson that the
    correction encodes a belief about the data.
12. **A quantitative scorecard** and **reusable `snv()` / `msc()` helpers**, with
    the one rule for new data: reuse the MSC reference, never refit it.

Closes with **Key Takeaways**, a **Practical Checklist**, **Common Mistakes**,
**Reporting Guidance**, and the **Next Lesson** pointer.

## Prerequisites

- 4.1 (Beer–Lambert and the Absorbance Mindset) — the absorbance mindset scatter
  distorts. Helpful but not required.
- 3.2 (Savitzky–Golay Smoothing and Derivatives) — derivatives are the other half
  of an NIR preprocessing chain (assembled in 4.7). Helpful but not required.
- 6.3 (PCA) is previewed here via a from-scratch SVD; no prior PCA needed.

## How to run

From the repository root, once:

```bash
pip install -e ".[notebooks]"
```

Then open and run this notebook from this folder, top to bottom. It needs no
external data — every spectrum is generated from a fixed seed (`SEED = 4`), so your
figures and printed numbers match the committed output. PCA is done with NumPy's
SVD, so no `scikit-learn` is required. The `exports/` folder it creates (PNG
figures) is regenerable scratch and is git-ignored.

## Data

Simulated NIR spectra via `from simulated_data import nir`. A `make_nir_set()`
helper threads one shared NumPy generator through `nir.simulate()` to build two
labeled sets: the **primary** band-ratio set (three broad fixed matrix bands at
1450 / 1930 / 2250 nm plus a diagnostic 1720 nm analyte band whose height encodes
the property) and a **global-level** set used only for the "when correction hurts"
demonstration. Every sample's true multiplicative slope and additive offset are
recorded in `meta` and used as the answer key. No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 4.3
- Previous: [4.2 — UV–Vis: Building Your First Calibration Curve](../4.2_calibration_curve_with_lod_loq/)
- Follow-up: 4.7 — Building a Reusable Spectral Preprocessing Pipeline *(planned)*;
  feeds 6.3 (PCA) and 6.5 (PLS)
