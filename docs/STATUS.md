# Project Status

_Last updated: 2026-06-16_

A snapshot of what exists today: notebooks drafted, simulator modules built, and
tests passing. The live lesson index is [`../notebooks/README.md`](../notebooks/README.md).

**Status key:** 🟢 Reviewed · 🟡 Drafted · ⬜ Planned

---

## Completed notebooks (drafted, 🟡)

| ID | Title | Data source |
|----|-------|-------------|
| 1.1 | [Why Python Belongs on the Lab Bench](../notebooks/01_foundations/1.1_why_python_on_the_lab_bench/) | inline toy data |
| 1.2 | [Notebooks, Scripts, and How to Not Lose Your Work](../notebooks/01_foundations/1.2_notebooks_scripts_and_reproducibility/) | inline toy data |
| 1.3 | [Variables, Numbers, and Units Without Tears](../notebooks/01_foundations/1.3_variables_numbers_and_units/) | inline toy data |
| 1.4 | [Lists, Arrays, and a First Spectrum](../notebooks/01_foundations/1.4_lists_arrays_and_a_first_spectrum/) | inline toy data |
| 1.5 | [Loops and Conditionals for Batch Thinking](../notebooks/01_foundations/1.5_loops_and_conditionals_for_batch_thinking/) | inline toy data |
| 1.6 | [Functions: Writing a Step Once and Reusing It](../notebooks/01_foundations/1.6_functions_write_once_reuse/) | inline toy data |
| 2.1 | [NumPy Arrays: Math on Whole Spectra at Once](../notebooks/02_scientific_computing/2.1_numpy_arrays_whole_spectra/) | inline toy data |
| 2.2 | [Indexing, Slicing, and Selecting Spectral Regions](../notebooks/02_scientific_computing/2.2_indexing_slicing_spectral_regions/) | inline toy data |
| 2.3 | [pandas DataFrames for Sample Tables](../notebooks/02_scientific_computing/2.3_pandas_dataframes_sample_tables/) | inline toy data |
| 2.4 | [Reading Real Instrument Files](../notebooks/02_scientific_computing/2.4_reading_instrument_files/) | `uvvis` |
| 2.5 | [Plotting That Reveals Chemistry](../notebooks/02_scientific_computing/2.5_plotting_that_reveals_chemistry/) | `uvvis` |
| 2.6 | [Missing Values and Detector Dropouts](../notebooks/02_scientific_computing/2.6_missing_values_and_detector_dropouts/) | inline toy data |
| 2.7 | [Joining Measurements and Metadata](../notebooks/02_scientific_computing/2.7_joining_measurements_and_metadata/) | inline toy data |
| 2.8 | [Reshaping Data for Analysis](../notebooks/02_scientific_computing/2.8_reshaping_data_for_analysis/) | inline toy data |
| 3.1 | [Noise, Signal, and Why Preprocessing Exists](../notebooks/03_signal_processing/3.1_noise_signal_and_preprocessing/) | inline toy data |
| 3.2 | [Savitzky–Golay Smoothing and Derivatives](../notebooks/03_signal_processing/3.2_savgol_smoothing_derivatives/) | `uvvis` |
| 3.3 | [Asymmetric Least Squares (AsLS) Baseline Correction](../notebooks/03_signal_processing/3.3_asls_baseline_correction/) | `uvvis` |
| 3.4 | [Peak Detection and Picking](../notebooks/03_signal_processing/3.4_peak_detection_and_picking/) | `uvvis` |
| 3.5 | [Peak Integration and Quantifying Area](../notebooks/03_signal_processing/3.5_peak_integration_and_quantitation/) | `uvvis` |
| 3.6 | [Signal Averaging and the √N Rule](../notebooks/03_signal_processing/3.6_signal_averaging_sqrt_n_rule/) | inline toy data |
| 3.7 | [Frequency Domain: A Practical Look at the FFT](../notebooks/03_signal_processing/3.7_frequency_domain_fft/) | inline toy data |
| 4.2 | [UV–Vis: Building Your First Calibration Curve](../notebooks/04_spectroscopy/4.2_calibration_curve_with_lod_loq/) | `uvvis` |
| 4.3 | [NIR Preprocessing: SNV, MSC, and Scatter Correction](../notebooks/04_spectroscopy/4.3_nir_snv_msc_scatter_correction/) | `nir` |
| 4.5 | [Raman: Cosmic Ray Removal and Fluorescence Baselines](../notebooks/04_spectroscopy/4.5_raman_cosmic_ray_fluorescence/) | `raman` |
| 6.3 | [PCA I: Scores, Loadings, and Seeing Structure](../notebooks/06_chemometrics/6.3_pca_scores_loadings/) | `core` + `nir` |
| 6.4 | [PCA II: Diagnostics and Outliers](../notebooks/06_chemometrics/6.4_pca_diagnostics_and_outliers/) | `core` + `artifacts` |
| 6.5 | [PLS Regression: Quantitative Prediction from Spectra](../notebooks/06_chemometrics/6.5_pls_regression/) | `core` |

27 notebooks drafted. The simulator-backed notebooks run offline from a fixed seed and
grade themselves against the simulator's ground truth; the Track 1 foundations
(1.1–1.6), the Track 2 data-handling notebooks (2.1–2.3, 2.6–2.8), and the new Track 3
notebooks (3.1, 3.6, 3.7) use inline generated data only and do not require the
`simulated_data` package.

> **Track 3 additions (2026-06-16).** Added **3.1 — Noise, Signal, and Why
> Preprocessing Exists** (the Track 3 opener; broadens curriculum.md's smoothing-only
> 3.1 into a "why preprocessing exists" overview, while still demonstrating the
> moving-average noise/resolution trade-off), a moat lesson **3.6 — Signal Averaging
> and the √N Rule** (not in `docs/curriculum.md`), and **3.7 — Frequency Domain: A
> Practical Look at the FFT**. Current Track 3 index order: 3.1 → 3.6 (√N) → 3.7 (FFT),
> with **Peak Fitting now planned at 3.8**. Human follow-ups:
> (1) `docs/curriculum.md` still shows the original Track 3 numbering (Peak Fitting 3.6,
> FFT 3.7, no Signal Averaging) — reconcile it to this order.
> (2) Two existing notebooks have **stale "Next Lesson" links** (left untouched to avoid
> rewriting completed notebooks): **3.5** points to "3.6 — Peak Fitting" (now Signal
> Averaging), and **3.6** points to "3.7 — Peak Fitting" (now FFT).
> (3) The core Track 3 signal-processing arc (3.1–3.7) is now complete; only the
> advanced **Peak Fitting (3.8)** remains planned.

> **Track 2 restructure (2026-06-16).** This sprint added 2.1–2.3 (matching the
> curriculum) and **redefined the later Track 2 lessons**: 2.6 is now *Missing Values
> and Detector Dropouts*, 2.7 is *Joining Measurements and Metadata*, and a new **2.8
> — Reshaping Data for Analysis** carries the reshaping content previously planned
> under 2.6. The earlier planned **2.7 — Saving Results: Arrays, Tables, and Figures**
> is **not yet scheduled** under a new ID. `docs/curriculum.md` still describes the old
> 2.6/2.7 and has no 2.8 — it needs a human pass to match this structure, and the
> existing 2.5 notebook's "Next Lesson" still points to the old 2.6 title.

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
