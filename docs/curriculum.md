# Python for Analytical Chemists — Complete Curriculum

A nine-track, build-as-you-go curriculum. Each track assumes the ones before it. Within a track, lessons are ordered so every concept rests on something already taught. The spine is the analytical workflow itself: get data in → handle it numerically → clean the signal → interpret it by technique → model it → put it to work in the lab.

**Difficulty key:** Beginner (no prior coding needed) · Intermediate (comfortable with NumPy/pandas) · Advanced (comfortable with modeling and validation).

**How to read a lesson:** *Objective* = what the viewer can do afterward. *Scientific motivation* = the measurement problem that justifies it. *Prerequisites* = the lessons that must come first.

---

## Track 1 — Foundations

The goal of this track is not to teach programming. It is to get a lab scientist from "I have a data file" to "I can manipulate it in Python" with the smallest possible vocabulary.

### 1.1 — Why Python Belongs on the Lab Bench
- **Objective:** Set up Python, run a notebook, and load a real spectrum in under ten minutes.
- **Scientific motivation:** Vendor software hides your data behind menus and locks you to one instrument. Python gives you a transparent, reproducible alternative you own.
- **Prerequisites:** None.
- **Difficulty:** Beginner.
- **Length:** 10–12 min.

### 1.2 — Notebooks, Scripts, and How to Not Lose Your Work
- **Objective:** Use Jupyter cells, save and re-run a notebook, and know when to use a script instead.
- **Scientific motivation:** Reproducibility starts with being able to re-run an analysis and get the same number. A notebook is a lab notebook for data.
- **Prerequisites:** 1.1.
- **Difficulty:** Beginner.
- **Length:** 8–10 min.

### 1.3 — Variables, Numbers, and Units Without Tears
- **Objective:** Store measurements in variables, do arithmetic, and keep track of units explicitly.
- **Scientific motivation:** Most lab errors are unit errors. Naming and typing your quantities makes wrong answers visible.
- **Prerequisites:** 1.2.
- **Difficulty:** Beginner.
- **Length:** 10–12 min.

### 1.4 — Lists, Arrays, and a First Spectrum
- **Objective:** Hold a wavelength axis and an intensity axis as paired sequences and plot one against the other.
- **Scientific motivation:** Every spectrum and chromatogram is just two aligned columns: an x-axis you control and a y-axis you measure.
- **Prerequisites:** 1.3.
- **Difficulty:** Beginner.
- **Length:** 12–14 min.

### 1.5 — Loops and Conditionals for Batch Thinking
- **Objective:** Process many samples with a loop and make decisions with `if` statements.
- **Scientific motivation:** Labs rarely measure one sample. The moment you have a tray of 96, you need to do the same thing to each one without copy-paste.
- **Prerequisites:** 1.4.
- **Difficulty:** Beginner.
- **Length:** 12–15 min.

### 1.6 — Functions: Writing a Step Once and Reusing It
- **Objective:** Wrap a preprocessing step in a function and call it on any spectrum.
- **Scientific motivation:** A method should be defined once and applied identically everywhere. Functions are how you make a method portable and testable.
- **Prerequisites:** 1.5.
- **Difficulty:** Beginner.
- **Length:** 12–15 min.

---

## Track 2 — Scientific Computing

This track gives you the numerical and data-handling tools that everything afterward depends on: NumPy for math on arrays, pandas for tables, and matplotlib for seeing what you have.

### 2.1 — NumPy Arrays: Math on Whole Spectra at Once
- **Objective:** Add, scale, slice, and reduce arrays without writing loops.
- **Scientific motivation:** Vectorized math is how you baseline-subtract a thousand spectra in one line — and it mirrors how you think about signals mathematically.
- **Prerequisites:** 1.6.
- **Difficulty:** Beginner.
- **Length:** 14–16 min.

### 2.2 — Indexing, Slicing, and Selecting Spectral Regions
- **Objective:** Extract a wavenumber window, mask a detector gap, and find the index of a peak.
- **Scientific motivation:** Real analysis happens in regions of interest — a fingerprint band, an analyte peak, a quiet baseline window.
- **Prerequisites:** 2.1.
- **Difficulty:** Beginner.
- **Length:** 12–14 min.

### 2.3 — pandas DataFrames for Sample Tables
- **Objective:** Load a table of samples and metadata, filter rows, and compute per-group summaries.
- **Scientific motivation:** Your measurements always travel with metadata — batch, operator, instrument, concentration. Keeping signal and metadata together prevents mix-ups.
- **Prerequisites:** 2.1.
- **Difficulty:** Beginner.
- **Length:** 15–18 min.

### 2.4 — Reading Real Instrument Files (CSV, TXT, and the Messy Ones)
- **Objective:** Import exported spectra and chromatograms, skip header junk, and parse delimiters correctly.
- **Scientific motivation:** The first wall every scientist hits is a file that won't load cleanly. Decoding vendor exports is a core skill, not a footnote.
- **Prerequisites:** 2.3.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.
- **Video:** https://youtu.be/grI2bnXnfAQ

### 2.5 — Plotting That Reveals Chemistry
- **Objective:** Build labeled spectral plots, overlays, and shaded regions you'd put in a paper.
- **Scientific motivation:** A good plot is an analytical instrument. Overlays expose batch differences; shading marks integration windows.
- **Prerequisites:** 2.2, 2.3.
- **Difficulty:** Intermediate.
- **Length:** 15–18 min.
- **Video:** https://youtu.be/yMSNV9NwwCk

### 2.6 — Tidy Data and Reshaping Spectral Matrices
- **Objective:** Move between long and wide formats and assemble a samples-by-variables matrix.
- **Scientific motivation:** Chemometric tools expect a clean matrix: one row per sample, one column per wavelength. Getting there is half the battle.
- **Prerequisites:** 2.4.
- **Difficulty:** Intermediate.
- **Length:** 14–16 min.

### 2.7 — Saving Results: Arrays, Tables, and Figures
- **Objective:** Persist processed data and figures in formats colleagues can open.
- **Scientific motivation:** An analysis nobody can reopen is worthless. Reproducible output is the close of every workflow.
- **Prerequisites:** 2.5, 2.6.
- **Difficulty:** Beginner.
- **Length:** 10–12 min.

---

## Track 3 — Signal Processing

This is the preprocessing that decides whether any downstream model works at all. Taught generally here, then specialized per technique in later tracks.

> **Built sequence note (2026-06-16).** Track 3 was reorganized during the build
> sprints from its original plan. Signal Averaging (the √N rule) was added as a moat
> lesson at 3.6, and the section now runs 3.1 → 3.7 with Peak Fitting moved to 3.8
> (planned). The numbering below reflects what is actually built.

### 3.1 — Noise, Signal, and Why Preprocessing Exists
- **Objective:** Name the nuisance components in a raw spectrum (noise, baseline, drift, artifacts), tell signal from nuisance, and understand the moving-average noise/resolution trade-off — framed as why preprocessing exists at all.
- **Scientific motivation:** A raw measurement is signal + nuisance. Preprocessing is the scientific judgment of separating them — reveal real chemistry or fabricate it. Every later Track 3 step exists because of this.
- **Prerequisites:** 2.2.
- **Difficulty:** Intermediate.
- **Length:** 14–16 min.

### 3.2 — Savitzky–Golay Smoothing and Derivatives
- **Objective:** Apply SG smoothing and compute first and second derivatives correctly.
- **Scientific motivation:** SG is the workhorse of spectroscopy: it smooths while preserving peak shape, and its derivatives remove baseline offset and sharpen overlapping bands.
- **Prerequisites:** 3.1.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 3.3 — Baseline Correction Fundamentals (AsLS)
- **Objective:** Remove a sloping or curved baseline with polynomial and asymmetric least-squares (AsLS) methods.
- **Scientific motivation:** Baseline drift biases peak area and ruins quantitation. Correct it wrong and you bias the result; correct it well and quantitation becomes honest.
- **Prerequisites:** 3.2.
- **Difficulty:** Intermediate.
- **Length:** 18–20 min.

### 3.4 — Peak Detection and Picking
- **Objective:** Locate peaks by height, prominence, and distance, and reject noise spikes.
- **Scientific motivation:** Peaks are where the chemistry is. Reliable, tunable peak finding underlies identification, integration, and quantitation.
- **Prerequisites:** 3.2.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 3.5 — Peak Integration and Quantifying Area
- **Objective:** Define integration limits and compute peak area with a local baseline.
- **Scientific motivation:** Area, not height, is what scales with amount in chromatography and much of spectroscopy. How you draw the baseline under a peak changes the number you report.
- **Prerequisites:** 3.3, 3.4.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 3.6 — Signal Averaging and the √N Rule: When More Scans Help and When They Don't
- **Objective:** Measure the √N signal-to-noise improvement under ideal white noise, and see it break under drift, correlated noise, or a changing sample.
- **Scientific motivation:** Co-adding scans is the most common SNR move in spectroscopy and MS, and it silently fails when noise isn't white or the sample isn't stable. Knowing when √N holds — and when more scans mislead — is measurement judgment, not code.
- **Prerequisites:** 3.1.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 3.7 — Frequency Domain: A Practical Look at the FFT
- **Objective:** Read a signal in the time and frequency domains, use the FFT to find periodic interference, and avoid aliasing and spectral leakage.
- **Scientific motivation:** Mains hum, pump pulsation, instrument oscillation, and daily sensor rhythms show up as sharp, locatable frequency peaks — and a peak can lie if you undersample or skip windowing.
- **Prerequisites:** 3.1.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 3.8 — Peak Fitting with Gaussians, Lorentzians, and Voigt *(planned)*
- **Objective:** Fit single and overlapping peaks to a model and extract position, width, and area.
- **Scientific motivation:** Overlapping bands can't be integrated by eye. Fitting a physical line shape separates them and gives uncertainty on each parameter.
- **Prerequisites:** 3.5.
- **Difficulty:** Advanced.
- **Length:** 20–24 min.

---

## Track 4 — Spectroscopy

Now the general tools meet specific techniques. Each lesson uses the preprocessing from Track 3 in the way that technique actually demands.

### 4.1 — Beer–Lambert and the Absorbance Mindset
- **Objective:** Convert transmittance to absorbance and reason about linearity and saturation.
- **Scientific motivation:** Quantitative spectroscopy lives or dies on the linear absorbance–concentration relationship and knowing when it breaks.
- **Prerequisites:** 2.5.
- **Difficulty:** Beginner.
- **Length:** 12–14 min.

### 4.2 — UV–Vis: Building Your First Calibration Curve
- **Objective:** Fit a calibration line, compute concentration of unknowns, and report uncertainty.
- **Scientific motivation:** The calibration curve is the most common quantitative task in the lab; doing it with honest error bars is a defensible result.
- **Prerequisites:** 4.1.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 4.3 — NIR Preprocessing: SNV, MSC, and Scatter Correction
- **Objective:** Apply standard normal variate and multiplicative scatter correction and see why NIR needs them.
- **Scientific motivation:** NIR spectra are dominated by physical scatter from particle size and packing. Removing it is the difference between a model that transfers and one that doesn't.
- **Prerequisites:** 3.2, 2.6.
- **Difficulty:** Intermediate.
- **Length:** 18–20 min.

### 4.4 — IR/FTIR: Atmospheric Correction and Band Assignment
- **Objective:** Remove water and CO₂ bands and map peaks to functional groups programmatically.
- **Scientific motivation:** FTIR fingerprints chemistry, but atmospheric bands and baseline curvature obscure it; cleaning them up makes assignment reliable.
- **Prerequisites:** 3.3, 3.4.
- **Difficulty:** Intermediate.
- **Length:** 18–20 min.

### 4.5 — Raman: Cosmic Ray Removal and Fluorescence Baselines
- **Objective:** Despike cosmic rays and subtract strong fluorescence backgrounds.
- **Scientific motivation:** Raman's two signature problems — sharp cosmic spikes and broad fluorescence — both masquerade as signal if untreated.
- **Prerequisites:** 3.3, 3.4.
- **Difficulty:** Advanced.
- **Length:** 18–22 min.

### 4.6 — Reading Proprietary Spectral Formats (.wdf, .spc, JCAMP-DX)
- **Objective:** Convert vendor spectral files into clean pandas/NumPy objects.
- **Scientific motivation:** The data you most want is often locked in a vendor format. Liberating it into Python is the gateway to every method in this course.
- **Prerequisites:** 2.4.
- **Difficulty:** Advanced.
- **Length:** 18–22 min.

### 4.7 — Building a Reusable Spectral Preprocessing Pipeline
- **Objective:** Chain trimming, baseline, scatter correction, and derivative into one configurable function.
- **Scientific motivation:** A documented, ordered preprocessing pipeline is what makes a spectroscopic method reproducible and auditable.
- **Prerequisites:** 4.3, 4.4, 4.5.
- **Difficulty:** Advanced.
- **Length:** 20–24 min.

---

## Track 5 — Mass Spectrometry

MS has its own data structures and scale. This track treats spectra and chromatograms as data objects you can open, clean, and quantify.

### 5.1 — How MS Data Is Structured: Scans, m/z, and Intensity
- **Objective:** Understand profile vs. centroid data and the scan/retention-time hierarchy.
- **Scientific motivation:** You can't analyze MS data you don't understand structurally; the scan-by-scan layout drives every later step.
- **Prerequisites:** 2.3.
- **Difficulty:** Intermediate.
- **Length:** 14–16 min.

### 5.2 — Opening mzML and Converting Vendor Files with msconvert
- **Objective:** Use msconvert to produce mzML and read it into Python with pyteomics.
- **Scientific motivation:** mzML is the open lingua franca of MS. Getting from a vendor `.raw` to mzML unlocks every open-source tool.
- **Prerequisites:** 5.1.
- **Difficulty:** Intermediate.
- **Length:** 18–20 min.

### 5.3 — Extracting Ion Chromatograms (XIC/EIC)
- **Objective:** Pull an extracted-ion chromatogram for a target m/z across retention time.
- **Scientific motivation:** The XIC is the basic unit of targeted MS quantitation; building it yourself demystifies the vendor "integrate" button.
- **Prerequisites:** 5.2, 3.4.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 5.4 — Centroiding, Peak Picking, and Mass Accuracy
- **Objective:** Convert profile spectra to centroids and assess mass error in ppm.
- **Scientific motivation:** Identification depends on accurate masses; understanding centroiding and ppm error keeps you from over-trusting a match.
- **Prerequisites:** 5.1, 3.4.
- **Difficulty:** Advanced.
- **Length:** 18–20 min.

### 5.5 — Isotope Patterns and Molecular Formula Reasoning
- **Objective:** Simulate isotope envelopes and use them to support or reject a formula.
- **Scientific motivation:** Isotope spacing and abundance are a built-in identity check that distinguishes real assignments from coincidences.
- **Prerequisites:** 5.4.
- **Difficulty:** Advanced.
- **Length:** 18–22 min.

### 5.6 — Targeted Quantitation: Calibration with Internal Standards
- **Objective:** Build a response-ratio calibration using an internal standard and quantify unknowns.
- **Scientific motivation:** Internal standards correct for injection and ionization variability — the foundation of trustworthy MS quantitation.
- **Prerequisites:** 5.3, 4.2.
- **Difficulty:** Advanced.
- **Length:** 18–22 min.

### 5.7 — Aligning and Comparing Many Runs
- **Objective:** Correct retention-time drift and align features across a sample set.
- **Scientific motivation:** Untargeted comparison requires that the same feature line up across runs; alignment is what makes a feature table meaningful.
- **Prerequisites:** 5.3, 2.6.
- **Difficulty:** Advanced.
- **Length:** 20–24 min.

---

## Track 6 — Chemometrics

Multivariate methods explained so the math maps to chemistry. This track turns the clean matrices from Tracks 4–5 into interpretable models.

### 6.1 — Why Multivariate? The Limits of One Wavelength
- **Objective:** Show how using a full spectrum beats single-wavelength analysis.
- **Scientific motivation:** Real samples have overlapping, interfering signals; multivariate methods use the whole spectrum to separate what one channel can't.
- **Prerequisites:** 2.6, 4.7.
- **Difficulty:** Intermediate.
- **Length:** 14–16 min.

### 6.2 — Mean-Centering, Scaling, and Why Order Matters
- **Objective:** Apply column centering and scaling and explain their effect on a model.
- **Scientific motivation:** Preprocessing choices change what a model "sees" as important; getting them wrong silently biases every downstream result.
- **Prerequisites:** 6.1.
- **Difficulty:** Intermediate.
- **Length:** 14–16 min.

### 6.3 — PCA I: Scores, Loadings, and Seeing Structure
- **Objective:** Run PCA and read scores and loadings as sample groupings and spectral drivers.
- **Scientific motivation:** PCA is the first look at any dataset — it reveals clusters, trends, and outliers before you commit to a model.
- **Prerequisites:** 6.2.
- **Difficulty:** Intermediate.
- **Length:** 18–20 min.

### 6.4 — PCA II: Outlier Detection and Diagnostics
- **Objective:** Use Hotelling's T² and Q-residuals to flag anomalous samples.
- **Scientific motivation:** A single bad spectrum can wreck a calibration; PCA diagnostics catch it with statistical justification.
- **Prerequisites:** 6.3.
- **Difficulty:** Advanced.
- **Length:** 16–18 min.

### 6.5 — PLS Regression: Quantitative Prediction from Spectra
- **Objective:** Build and interpret a PLS model relating spectra to a measured property.
- **Scientific motivation:** PLS is the standard for spectroscopic quantitation — predicting concentration or quality from a full spectrum.
- **Prerequisites:** 6.3.
- **Difficulty:** Advanced.
- **Length:** 20–24 min.

### 6.6 — Validation Done Right: Cross-Validation, RMSEP, and Overfitting
- **Objective:** Choose latent variables by cross-validation and report honest prediction error.
- **Scientific motivation:** An optimistic model that fails on new samples is worse than no model; rigorous validation is what makes a calibration trustworthy.
- **Prerequisites:** 6.5.
- **Difficulty:** Advanced.
- **Length:** 20–22 min.

### 6.7 — Calibration Transfer Between Instruments
- **Objective:** Apply piecewise direct standardization to move a model between instruments.
- **Scientific motivation:** A model built on one instrument rarely works on another; transfer methods rescue months of calibration work.
- **Prerequisites:** 6.6, 4.7.
- **Difficulty:** Advanced.
- **Length:** 22–26 min.

---

## Track 7 — Machine Learning

ML framed as an extension of chemometrics, with the same insistence on validation and interpretability. No black boxes for their own sake.

### 7.1 — Classification Basics: Identifying Sample Classes
- **Objective:** Train and evaluate a classifier that separates material types from spectra.
- **Scientific motivation:** Pass/fail, authentic/adulterated, polymorph A/B — classification answers the qualitative questions labs ask daily.
- **Prerequisites:** 6.3.
- **Difficulty:** Intermediate.
- **Length:** 18–20 min.

### 7.2 — Train/Test Splits, Leakage, and Trustworthy Accuracy
- **Objective:** Split data correctly, avoid leakage from replicates and preprocessing, and read a confusion matrix.
- **Scientific motivation:** Replicates and batch structure make naive accuracy a lie; correct splitting is what makes a reported number real.
- **Prerequisites:** 7.1.
- **Difficulty:** Advanced.
- **Length:** 18–20 min.

### 7.3 — Feature Importance and Keeping Models Interpretable
- **Objective:** Identify which spectral regions drive a prediction and sanity-check them chemically.
- **Scientific motivation:** A model that predicts well for the wrong reasons will fail unpredictably; tying features to chemistry builds trust.
- **Prerequisites:** 7.2.
- **Difficulty:** Advanced.
- **Length:** 16–18 min.

### 7.4 — Anomaly and Novelty Detection
- **Objective:** Flag samples that don't belong to any known class or distribution.
- **Scientific motivation:** Contamination, instrument faults, and new impurities show up as anomalies before they show up as failures.
- **Prerequisites:** 6.4, 7.2.
- **Difficulty:** Advanced.
- **Length:** 18–20 min.

### 7.5 — Imbalanced Data and Rare-Event Problems
- **Objective:** Handle datasets where the class you care about is rare without fooling yourself on accuracy.
- **Scientific motivation:** Defects and adulterants are rare by definition; standard accuracy hides exactly the cases you most need to catch.
- **Prerequisites:** 7.2.
- **Difficulty:** Advanced.
- **Length:** 16–18 min.

### 7.6 — When ML Is the Wrong Tool
- **Objective:** Recognize cases where PLS, a calibration curve, or a physical model beats ML.
- **Scientific motivation:** Reaching for ML when a linear model suffices adds risk and opacity for no gain; method choice is a scientific judgment.
- **Prerequisites:** 7.3, 6.6.
- **Difficulty:** Advanced.
- **Length:** 14–16 min.

---

## Track 8 — Sensor Analytics

Time-series and multivariate sensor data: drift, calibration, and turning streams of readings into decisions.

### 8.1 — Working with Time-Series Sensor Data
- **Objective:** Load timestamped sensor logs, resample, and handle gaps.
- **Scientific motivation:** Sensors produce irregular, drifting streams; getting them onto a clean time axis is the precondition for any analysis.
- **Prerequisites:** 2.3.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 8.2 — Smoothing and Drift Correction for Sensors
- **Objective:** Separate slow drift from real change and correct baseline wander over time.
- **Scientific motivation:** Sensor drift mimics process change; distinguishing the two prevents false alarms and missed events.
- **Prerequisites:** 8.1, 3.3.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 8.3 — Multivariate Sensor Arrays and the Electronic Nose
- **Objective:** Treat an array of sensors as a multivariate fingerprint and cluster responses.
- **Scientific motivation:** Single sensors are non-specific; arrays gain selectivity only when analyzed together, exactly as in chemometrics.
- **Prerequisites:** 8.2, 6.3.
- **Difficulty:** Advanced.
- **Length:** 18–20 min.

### 8.4 — Real-Time Process Monitoring and Control Charts
- **Objective:** Build control limits and detect out-of-spec conditions as data arrives.
- **Scientific motivation:** Process analytical technology depends on catching excursions live, not in a post-mortem.
- **Prerequisites:** 8.2.
- **Difficulty:** Advanced.
- **Length:** 18–20 min.

### 8.5 — Predictive Maintenance from Sensor Signatures
- **Objective:** Use anomaly detection on sensor trends to anticipate instrument faults.
- **Scientific motivation:** Instruments degrade with measurable signatures; spotting them early protects data quality and uptime.
- **Prerequisites:** 8.4, 7.4.
- **Difficulty:** Advanced.
- **Length:** 18–20 min.

---

## Track 9 — Real Laboratory Workflows

Tying everything together into reproducible, shareable, automatable pipelines — the close of the whole curriculum.

### 9.1 — From Notebook to Reusable Script
- **Objective:** Refactor an exploratory notebook into a parameterized script that runs end to end.
- **Scientific motivation:** A one-off analysis becomes a method only when it runs the same way, unattended, every time.
- **Prerequisites:** 4.7, 6.6.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 9.2 — Batch Processing a Folder of Samples
- **Objective:** Loop a full pipeline over a directory of files and collect results into one table.
- **Scientific motivation:** Real throughput means processing trays and campaigns, not single files; automation removes transcription error.
- **Prerequisites:** 9.1.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 9.3 — Automated Reporting and Figures
- **Objective:** Generate a formatted report with results, plots, and pass/fail flags automatically.
- **Scientific motivation:** Consistent, auto-generated reports save hours and remove the formatting errors that creep into manual ones.
- **Prerequisites:** 9.2, 2.7.
- **Difficulty:** Intermediate.
- **Length:** 16–18 min.

### 9.4 — Data Integrity, Provenance, and Reproducibility
- **Objective:** Record inputs, parameters, and versions so any result can be traced and reproduced.
- **Scientific motivation:** In regulated and rigorous environments, a result you can't trace is a result you can't defend.
- **Prerequisites:** 9.3.
- **Difficulty:** Advanced.
- **Length:** 16–18 min.

### 9.5 — Connecting to LIMS, Databases, and Shared Storage
- **Objective:** Read from and write results to shared lab systems programmatically.
- **Scientific motivation:** Analysis that lives only on one laptop doesn't scale; integration is what turns scripts into lab infrastructure.
- **Prerequisites:** 9.2.
- **Difficulty:** Advanced.
- **Length:** 18–20 min.

### 9.6 — Building a Complete Method, End to End (Capstone)
- **Objective:** Take raw vendor files to a validated, reported result in one reproducible pipeline.
- **Scientific motivation:** This is the whole mission in one project: raw measurements turned into defensible meaning, automatically.
- **Prerequisites:** 9.4, 6.7, 7.6.
- **Difficulty:** Advanced.
- **Length:** 24–30 min.

---

## Suggested Progression

Tracks 1–3 are the universal base and should be taken in order by anyone. From Track 4 onward, viewers can branch by technique — a spectroscopist can run 4 → 6 → 7 → 9, while an MS analyst runs 5 → 6 → 7 → 9 — but the chemometrics, ML, and workflow tracks assume the relevant technique track is done first. The Track 9 capstone (9.6) is designed as the series finale that revisits one example through every stage.
