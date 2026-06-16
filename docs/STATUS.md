# Project Status

_Last updated: 2026-06-15_

A snapshot of what exists today: notebooks drafted, simulator modules built, and
tests passing. The live lesson index is [`../notebooks/README.md`](../notebooks/README.md).

**Status key:** 🟢 Reviewed · 🟡 Drafted · ⬜ Planned

---

## Completed notebooks (drafted, 🟡)

| ID | Title | Data source |
|----|-------|-------------|
| 2.4 | [Reading Real Instrument Files](../notebooks/02_scientific_computing/2.4_reading_instrument_files/) | `uvvis` |
| 2.5 | [Plotting That Reveals Chemistry](../notebooks/02_scientific_computing/2.5_plotting_that_reveals_chemistry/) | `uvvis` |
| 3.2 | [Savitzky–Golay Smoothing and Derivatives](../notebooks/03_signal_processing/3.2_savgol_smoothing_derivatives/) | `uvvis` |
| 3.3 | [Asymmetric Least Squares (AsLS) Baseline Correction](../notebooks/03_signal_processing/3.3_asls_baseline_correction/) | `uvvis` |
| 3.4 | [Peak Detection and Picking](../notebooks/03_signal_processing/3.4_peak_detection_and_picking/) | `uvvis` |
| 3.5 | [Peak Integration and Quantifying Area](../notebooks/03_signal_processing/3.5_peak_integration_and_quantitation/) | `uvvis` |
| 4.2 | [UV–Vis: Building Your First Calibration Curve](../notebooks/04_spectroscopy/4.2_calibration_curve_with_lod_loq/) | `uvvis` |
| 4.3 | [NIR Preprocessing: SNV, MSC, and Scatter Correction](../notebooks/04_spectroscopy/4.3_nir_snv_msc_scatter_correction/) | `nir` |
| 4.5 | [Raman: Cosmic Ray Removal and Fluorescence Baselines](../notebooks/04_spectroscopy/4.5_raman_cosmic_ray_fluorescence/) | `raman` |
| 6.3 | [PCA I: Scores, Loadings, and Seeing Structure](../notebooks/06_chemometrics/6.3_pca_scores_loadings/) | `core` + `nir` |
| 6.4 | [PCA II: Diagnostics and Outliers](../notebooks/06_chemometrics/6.4_pca_diagnostics_and_outliers/) | `core` + `artifacts` |
| 6.5 | [PLS Regression: Quantitative Prediction from Spectra](../notebooks/06_chemometrics/6.5_pls_regression/) | `core` |

12 notebooks drafted. Every notebook runs offline from a fixed seed and grades
itself against the simulator's ground truth.

---

## Current simulator modules (`simulated_data/`)

**Shared foundation**
- `types.py` — the `Dataset` return type (x, X always-2D, y, meta, labels) with the
  shape-contract validation every notebook relies on.
- `_rng.py` — `resolve_rng(seed)`; the single point of reproducibility (int /
  Generator / None → `Generator`, never global state).
- `__init__.py` — public surface: re-exports `uvvis`, `nir`, and `Dataset`.

**Physics core (`simulated_data/core/`)**
- `axes.py` — `build_axis` (by count or by step).
- `peaks.py` — `gaussian`, `lorentzian`, `add_peaks` (FWHM-parameterized; Gaussian
  + Lorentzian via a shape dispatch; Voigt deferred).
- `baselines.py` — `sloping_baseline`, `curved_baseline`.
- `noise.py` — `gaussian_noise` (constant-sigma; shot/pink deferred).
- `scatter.py` — `apply_scatter` (per-sample multiplicative slope + additive
  offset; returns `(X_scattered, slope, offset)` so truth lands in `meta`).
- `background.py` — `fluorescence_background` (broad, smooth, AsLS-removable swell
  scaled to a given magnitude). Powers Raman.
- `artifacts.py` — `add_cosmic_rays` (sharp single-pixel spikes; returns
  `(y_spiked, indices)` so spike truth lands in `meta`). Powers Raman.

**Technique modules**
- `uvvis.py` — `simulate(...)`: Beer–Lambert bands + baseline + noise. Powers the
  Track 2/3 lessons and 4.2.
- `nir.py` — `simulate(...)`: broad overlapping bands + per-sample scatter + noise,
  with true scatter recorded in `meta`. Powers 4.3.
- `raman.py` — `simulate(...)`: sharp Lorentzian bands + broad fluorescence +
  cosmic-ray spikes + noise, with the true band profile, fluorescence curve, and
  spike indices recorded in `meta`. Powers 4.5.

**Not yet built (deferred until a notebook needs them):** Voigt peaks, shot/pink
noise, `core/artifacts` saturation + dropouts; technique modules
`chromatography.py`, `sensors.py`; the `uvvis.simulate_calibration_series` and
`nir.simulate_calibration_set` helpers; `Dataset.plot()`.

---

## Current tests (`tests/`) — 58 passing

- `test_simulated_data_phase1.py` (10) — `uvvis` + `Dataset`: import, shape
  contract, seed reproducibility, Beer–Lambert concentration scaling, baseline
  metadata, `to_frame`/`single`.
- `test_simulated_data_nir.py` (19) — `nir.simulate` (reproducibility, shape
  contract, broad/overlapping defaults, scatter metadata, exact reconstruction
  from recorded slope/offset) and `core.scatter.apply_scatter` (shape, zero-sigma
  identity, generator reproducibility, input validation).
- `test_simulated_data_raman.py` (29) — `core.peaks.lorentzian` (FWHM, height,
  heavy tails), `core.background.fluorescence_background` (broad/smooth, peak =
  magnitude, off-switch), `core.artifacts.add_cosmic_rays` (count/indices truth,
  no-op + RNG-stream preservation at zero spikes, input validation), and
  `raman.simulate` (reproducibility, shape contract, fluorescence dominates peaks,
  ground-truth metadata, peak-shape + cosmic-ray argument handling).

Run from the repo root with `pytest` (config in `pyproject.toml`).
