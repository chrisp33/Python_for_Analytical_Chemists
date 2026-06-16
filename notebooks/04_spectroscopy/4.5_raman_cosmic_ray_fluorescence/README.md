# 4.5 — Raman: Cosmic Ray Removal and Fluorescence Baselines

**Title:** *Is That a Peak or a Cosmic Ray? Cleaning Raman Properly*
**Track:** 4 — Spectroscopy · **Difficulty:** Intermediate · **Length:** 16–18 min · **Type:** Domain Moat

## Learning objective

Understand *why* raw Raman spectra carry a broad fluorescence background and
sharp cosmic-ray spikes, and clean both **correctly** — despiking the spikes and
baseline-correcting the fluorescence as the two distinct problems they are. The
lesson is deliberately not "call `despike()` and `baseline()` and move on." It
treats cleaning as a sequence of decisions with consequences: which artifact is
which, which tool removes it, in what order, and how hard to push before you start
deleting real chemistry. Because every spectrum comes from `raman.simulate()`,
the *true* band profile, the *true* fluorescence curve, and the *exact* spike
indices are known, so every step is graded against the right answer instead of
admired.

## Why it matters

Raman is exquisitely specific but practically weak: only about one photon in ten
million carries the vibrational fingerprint, so the chemistry routinely arrives
buried under two artifacts that are *larger than the signal*. Fluorescence — real
laser-excited emission from the sample or its impurities — is a broad swell that
can dwarf the bands; cosmic rays — particles striking the CCD — are single-pixel
spikes that masquerade as strong peaks. Handle them wrong and you either invent
peaks that aren't there or erase peaks that are. The notebook makes both the fix
and its failure modes **measurable**: spike detection at 100 % recall with zero
false alarms (the loudest real band reaching a z of ~4.7 against a threshold of
7), an AsLS baseline within ~1 % of the true fluorescence height, and a cleaned
spectrum within detector-noise distance of the truth (RMSE ≈ 0.035 on bands of
height 0.60). Then it breaks things on purpose: smoothing-before-despiking leaves
a **fake band ~3× taller** than any real peak; over-despiking flags **35 %** of
the spectrum and erodes band area; over-baseline-correction shrinks the strongest
band by **35 %**. The throughline: cosmic rays and fluorescence sit at opposite
ends of the width scale, and the tool that removes one is the wrong tool for the
other.

## What the notebook covers

1. **Why Raman carries both artifacts** — the weakness of Raman scattering makes
   laser-excited fluorescence (broad, smooth, real) and CCD cosmic rays (sharp,
   single-pixel, random) routinely larger than the bands.
2. **A realistic spectrum with ground truth** — `raman.simulate()` over
   200–3200 cm⁻¹ at high resolution with Lorentzian bands, fluorescence, spikes,
   and noise; the answer key (`clean_peaks`, `fluorescence_curve`,
   `cosmic_ray_indices`) read from `meta`.
3. **The raw spectrum** and **how both artifacts masquerade as signal** — a
   cosmic ray that looks like a tall peak, fluorescence shaped like a broad band.
4. **Why despiking ≠ baseline correction** — narrow/local/high-frequency vs
   broad/global/low-frequency; each tool is blind to the other's target.
5. **Spike detection by narrowness + intensity** — the modified z-score of the
   first difference (Whitaker–Hayes); graded against the true spike indices.
6. **Despiking without destroying bands** — interpolate the flagged pixels only;
   verify every other point is left bit-for-bit unchanged.
7. **Fluorescence baseline with AsLS** — the from-scratch asymmetric-least-squares
   fit (from 3.3), compared to the true fluorescence curve.
8. **Subtraction → corrected spectrum** — graded against the known bands.
9. **Why order matters** — smoothing before despiking spreads a spike into a fake
   band the despiker can no longer catch; despike first, always.
10. **Failure cases** — over-despiking (too-low threshold, too-wide window) and
    over-baseline-correction (`λ` too small), each quantified against truth.
11. **A reusable `clean_raman()` pipeline** — despike → AsLS subtract, with
    diagnostics, graded end-to-end.

Closes with **Key Takeaways**, a **Practical Checklist**, **Common Mistakes**,
**Reporting Guidance**, and the **Next Lesson** pointer.

## Prerequisites

- 3.3 (Asymmetric Least Squares Baseline Correction) — AsLS is reused here for the
  fluorescence baseline. Helpful but not required; the notebook re-states it.
- 3.4 (Peak Detection and Picking) — context for why a clean spectrum matters
  before you pick peaks. Helpful but not required.
- 3.2 (Savitzky–Golay Smoothing) — the smoothing used in the "order matters"
  demonstration. Helpful but not required.

## How to run

From the repository root, once:

```bash
pip install -e ".[notebooks]"
```

Then open and run this notebook from this folder, top to bottom. It needs no
external data — the spectrum is generated from a fixed seed (`SEED = 11`), so your
figures and printed numbers match the committed output. AsLS uses SciPy's sparse
solver; no `scikit-learn` is required. The `exports/` folder it creates (PNG
figures) is regenerable scratch and is git-ignored.

## Data

Simulated Raman spectrum via `from simulated_data import raman`. A single call to
`raman.simulate(fluorescence=3.0, cosmic_rays=4, noise=0.02, n_points=4000,
seed=11)` produces sharp Lorentzian bands on a broad fluorescence background with
four single-pixel cosmic rays and detector noise. The true band profile, the true
fluorescence curve, and the exact spike indices are recorded in `meta`
(`meta.attrs["clean_peaks"]`, `meta.attrs["fluorescence_curve"]`,
`meta["cosmic_ray_indices"]`) and used as the answer key. No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 4.5
- Previous: [4.3 — NIR Preprocessing: SNV, MSC, and Scatter Correction](../4.3_nir_snv_msc_scatter_correction/)
- Follow-up: 6.3 — PCA: Scores, Loadings, and Seeing Structure *(planned)*;
  cleaned Raman feeds chemometrics and, ultimately, spectral library matching
