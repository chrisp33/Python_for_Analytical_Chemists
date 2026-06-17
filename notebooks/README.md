# Notebook Library — Index

The live status board for every curriculum notebook. Notebooks are grouped by
track in zero-padded folders (`01_foundations/`, `02_scientific_computing/`, …);
each notebook keeps its bare curriculum ID as its filename, so the **filename
always points home** to the curriculum (see [`../docs/curriculum.md`](../docs/curriculum.md)).

Each lesson lives in its own folder alongside a `README.md`, plus `figures/` and
`data/` as needed.

**Status key:** ✅ Published · 🟡 Drafted (notebook complete, not filmed) · ⬜ Planned

## Setup (once)

Follow the [**Setup**](../README.md#setup) and
[**First notebook launch**](../README.md#first-notebook-launch) sections in the
root README. In short: create and activate a `.venv`, then from the repo root
run `python -m pip install -e ".[notebooks]"`. This installs the `simulated_data`
package editable, so every notebook can `from simulated_data import uvvis`
regardless of how deep it sits.

When you open a notebook, select the `.venv` kernel — and restart the kernel if
you just installed the package (see
[Troubleshooting](../README.md#troubleshooting)).

---

## Track 1 — Foundations
| ID | Title | Status |
|----|-------|--------|
| 1.1 | [Why Python Belongs on the Lab Bench](01_foundations/1.1_why_python_on_the_lab_bench/) | 🟡 |
| 1.2 | [Notebooks, Scripts, and How to Not Lose Your Work](01_foundations/1.2_notebooks_scripts_and_reproducibility/) | 🟡 |
| 1.3 | [Variables, Numbers, and Units Without Tears](01_foundations/1.3_variables_numbers_and_units/) | 🟡 |
| 1.4 | [Lists, Arrays, and a First Spectrum](01_foundations/1.4_lists_arrays_and_a_first_spectrum/) | 🟡 |
| 1.5 | [Loops and Conditionals for Batch Thinking](01_foundations/1.5_loops_and_conditionals_for_batch_thinking/) | 🟡 |
| 1.6 | [Functions: Writing a Step Once and Reusing It](01_foundations/1.6_functions_write_once_reuse/) | 🟡 |

## Track 2 — Scientific Computing
| ID | Title | Status |
|----|-------|--------|
| 2.1 | NumPy Arrays: Math on Whole Spectra at Once | ⬜ |
| 2.2 | Indexing, Slicing, and Selecting Spectral Regions | ⬜ |
| 2.3 | pandas DataFrames for Sample Tables | ⬜ |
| 2.4 | [Reading Real Instrument Files (CSV, TXT, and the Messy Ones)](02_scientific_computing/2.4_reading_instrument_files/) | 🟡 |
| 2.5 | [Plotting That Reveals Chemistry](02_scientific_computing/2.5_plotting_that_reveals_chemistry/) | 🟡 |
| 2.6 | Tidy Data and Reshaping Spectral Matrices | ⬜ |
| 2.7 | Saving Results: Arrays, Tables, and Figures | ⬜ |

## Track 3 — Signal Processing
| ID | Title | Status |
|----|-------|--------|
| 3.1 | Noise, Signal, and What Smoothing Really Does | ⬜ |
| 3.2 | [Savitzky–Golay Smoothing and Derivatives](03_signal_processing/3.2_savgol_smoothing_derivatives/) | 🟡 |
| 3.3 | [Asymmetric Least Squares (AsLS) Baseline Correction](03_signal_processing/3.3_asls_baseline_correction/) | 🟡 |
| 3.4 | [Peak Detection and Picking](03_signal_processing/3.4_peak_detection_and_picking/) | 🟡 |
| 3.5 | [Peak Integration and Quantifying Area](03_signal_processing/3.5_peak_integration_and_quantitation/) | 🟡 |
| 3.6 | Peak Fitting with Gaussians, Lorentzians, and Voigt | ⬜ |
| 3.7 | Frequency Domain: A Practical Look at the FFT | ⬜ |

## Track 4 — Spectroscopy
| ID | Title | Status |
|----|-------|--------|
| 4.1 | Beer–Lambert and the Absorbance Mindset | ⬜ |
| 4.2 | [UV–Vis: Building Your First Calibration Curve](04_spectroscopy/4.2_calibration_curve_with_lod_loq/) | 🟡 |
| 4.3 | [NIR Preprocessing: SNV, MSC, and Scatter Correction](04_spectroscopy/4.3_nir_snv_msc_scatter_correction/) | 🟡 |
| 4.4 | IR/FTIR: Atmospheric Correction and Band Assignment | ⬜ |
| 4.5 | [Raman: Cosmic Ray Removal and Fluorescence Baselines](04_spectroscopy/4.5_raman_cosmic_ray_fluorescence/) | 🟡 |
| 4.6 | Reading Proprietary Spectral Formats (.wdf, .spc, JCAMP-DX) | ⬜ |
| 4.7 | Building a Reusable Spectral Preprocessing Pipeline | ⬜ |

## Track 5 — Mass Spectrometry
| ID | Title | Status |
|----|-------|--------|
| 5.1 | How MS Data Is Structured: Scans, m/z, and Intensity | ⬜ |
| 5.2 | Opening mzML and Converting Vendor Files with msconvert | ⬜ |
| 5.3 | Extracting Ion Chromatograms (XIC/EIC) | ⬜ |
| 5.4 | Centroiding, Peak Picking, and Mass Accuracy | ⬜ |
| 5.5 | Isotope Patterns and Molecular Formula Reasoning | ⬜ |
| 5.6 | Targeted Quantitation: Calibration with Internal Standards | ⬜ |
| 5.7 | Aligning and Comparing Many Runs | ⬜ |

## Track 6 — Chemometrics
| ID | Title | Status |
|----|-------|--------|
| 6.1 | Why Multivariate? The Limits of One Wavelength | ⬜ |
| 6.2 | Mean-Centering, Scaling, and Why Order Matters | ⬜ |
| 6.3 | [PCA I: Scores, Loadings, and Seeing Structure](06_chemometrics/6.3_pca_scores_loadings/) | 🟡 |
| 6.4 | [PCA II: Outlier Detection and Diagnostics](06_chemometrics/6.4_pca_diagnostics_and_outliers/) | 🟡 |
| 6.5 | [PLS Regression: Quantitative Prediction from Spectra](06_chemometrics/6.5_pls_regression/) | 🟡 |
| 6.6 | Validation Done Right: Cross-Validation, RMSEP, and Overfitting | ⬜ |
| 6.7 | Calibration Transfer Between Instruments | ⬜ |

## Track 7 — Machine Learning
| ID | Title | Status |
|----|-------|--------|
| 7.1 | Classification Basics: Identifying Sample Classes | ⬜ |
| 7.2 | Train/Test Splits, Leakage, and Trustworthy Accuracy | ⬜ |
| 7.3 | Feature Importance and Keeping Models Interpretable | ⬜ |
| 7.4 | Anomaly and Novelty Detection | ⬜ |
| 7.5 | Imbalanced Data and Rare-Event Problems | ⬜ |
| 7.6 | When ML Is the Wrong Tool | ⬜ |

## Track 8 — Sensor Analytics
| ID | Title | Status |
|----|-------|--------|
| 8.1 | Working with Time-Series Sensor Data | ⬜ |
| 8.2 | Smoothing and Drift Correction for Sensors | ⬜ |
| 8.3 | Multivariate Sensor Arrays and the Electronic Nose | ⬜ |
| 8.4 | Real-Time Process Monitoring and Control Charts | ⬜ |
| 8.5 | Predictive Maintenance from Sensor Signatures | ⬜ |

## Track 9 — Real Laboratory Workflows
| ID | Title | Status |
|----|-------|--------|
| 9.1 | From Notebook to Reusable Script | ⬜ |
| 9.2 | Batch Processing a Folder of Samples | ⬜ |
| 9.3 | Automated Reporting and Figures | ⬜ |
| 9.4 | Data Integrity, Provenance, and Reproducibility | ⬜ |
| 9.5 | Connecting to LIMS, Databases, and Shared Storage | ⬜ |
| 9.6 | Building a Complete Method, End to End (Capstone) | ⬜ |

---

_This index reflects what currently exists. See [`../docs/STATUS.md`](../docs/STATUS.md)
for a snapshot of drafted notebooks, simulator modules, and test status._
