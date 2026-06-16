# 3.5 — Peak Integration and Quantifying Area

**Title:** *How Much Is There? Turning a Peak Into a Number*
**Track:** 3 — Signal Processing · **Difficulty:** Intermediate · **Length:** 18–20 min · **Type:** Foundation

## Learning objective

Turn a located band into a trustworthy **number** — its area — and understand
every decision that number depends on. The lesson is deliberately *not* "how to
call `numpy.trapezoid()`." It builds the reasoning around integration: area vs.
height, where to put the limits, why an uncorrected baseline biases every area,
how overlapping bands defeat splitting, how much the boundary choice contributes
to uncertainty, and how area becomes a calibration. Because every spectrum comes
from `uvvis.simulate()`, the *true* area (exact for a Gaussian) and *true*
concentration are known, so every result is graded against ground truth.

## Why it matters

Integration is where quantitation actually happens, and it is quietly full of
choices that change the answer. Height is one point and misleads the moment a
band's shape drifts; area uses the whole band and stays proportional to amount.
The trapezoidal rule is exact enough once a band is well sampled — so the error
that matters comes from the **limits** and the **baseline**, not the arithmetic.
The notebook makes this concrete and measurable: a modest sloping background
nearly *doubles* a raw area, and the bias grows with window width, so it can't be
integrated away. Correcting the baseline first (a local linear "drop", or AsLS
from 3.3) removes both the bias and most of the boundary sensitivity. The lesson
also draws an honest line: integration gives an exact *total* for overlapping
bands but cannot split them — that's a fitting problem (3.6) — and it closes by
building a calibration where integrated area recovers an unknown concentration
within ~1–2 %.

## What the notebook covers

1. **Area vs. height** — two bands with *identical area but different heights*
   (narrow-tall vs broad-short) show why area is the steadier measure of "how
   much" when shape can change.
2. **Numerical integration from scratch** — the trapezoidal rule written out by
   hand, shown identical to `np.trapezoid`, with a sampling-density convergence
   check.
3. **Integration boundaries** — `±1σ/±2σ/±3σ/full` windows on a clean band map
   directly onto the 68 / 95 / 99.7 % captured-area fractions; motivates a
   baseline-to-baseline (`±1.5·FWHM ≈ ±3.5σ`) window for corrected work.
4. **The baseline problem** — reconstructing the exact peak-only and
   baseline-only pieces to show raw integration = peak **+** background (+98 %
   bias here), and that the bias *grows* with window width.
5. **Correcting the baseline** — local linear "drop" between window endpoints
   (+0.3 %) and full AsLS from 3.3 (−0.6 %), both graded against the true peak
   area.
6. **Boundary uncertainty** — jittering the limits over 200 trials; baseline
   correction removes the bias *and* shrinks the spread (2.6 % → 0.9 %).
7. **Overlapping peaks** — the combined area is conserved (exact total) but the
   perpendicular-drop split is biased by several percent per band; true
   separation needs fitting (3.6).
8. **Area, concentration, and calibration** — a five-standard series is
   baseline-corrected and integrated; area-vs-concentration is linear
   (`R² ≈ 0.999`), the fitted slope matches the exact unit-band area to ~1 %, and
   an unknown is recovered within ~1–2 %. A broadening demo shows area staying
   constant while height varies ~2× at fixed amount.
9. **A reusable `integrate_peak()` helper** — local-linear baseline + trapezoid
   with sensible defaults, for later notebooks.

Closes with **Key Takeaways**, a **Practical Checklist**, **Common Mistakes**,
**Reporting Guidance**, and the **Next Lesson** pointer.

## Prerequisites

- 3.3 (AsLS Baseline Correction) and 3.4 (Peak Detection and Picking) — the
  baseline under a peak and the located band are exactly what we integrate here.
  3.3's AsLS routine is reused directly. Helpful but not required; the notebook
  re-imports what it needs.
- 2.4 / 2.5 (reading files and plotting) — helpful but not required.

## How to run

From the repository root, once:

```bash
pip install -e ".[notebooks]"
```

This pulls in SciPy (for the AsLS sparse solve). Then open and run this notebook
from this folder, top to bottom. It needs no external data — every spectrum is
generated from a fixed seed, so your figures match the committed output. The
`exports/` folder it creates (PNG figures) is regenerable scratch and is
git-ignored.

## Data

Simulated UV-Vis spectra via `from simulated_data import uvvis`. A clean band
(550 nm, FWHM 50) anchors the area/height and boundary sections; the same band on
a sloping baseline (`seed=5`) drives the baseline-bias and correction sections; a
two-band overlap (540/585 nm, `seed=2`) shows the splitting limit; and a
five-standard calibration series (`seed=7`) plus a blind unknown (`seed=99`)
close the loop on quantitation. The exact Gaussian area
(`amplitude · FWHM · √(π/4ln2)`) and the known concentrations are the answer key.
No external datasets.

## Links

- Curriculum: [`docs/curriculum.md`](../../../docs/curriculum.md) → 3.5
- Previous: [3.4 — Peak Detection and Picking](../3.4_peak_detection_and_picking/)
- Follow-up: 3.6 — Peak Fitting with Gaussians, Lorentzians, and Voigt *(planned)*
