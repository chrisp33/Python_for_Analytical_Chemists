# `simulated_data` — Architecture Design

The simulated-data package is the foundation the whole notebook library rests on. Dozens of lessons will import from it, so the design goal is a small set of scientifically honest primitives that compose into realistic spectra, chromatograms, and sensor streams — with every "knob" a lesson might want to teach (noise, baseline, peaks, scatter, fluorescence, drift) exposed through one consistent vocabulary.

This document defines the architecture. It does **not** implement the generators yet — it fixes the structure, the API surface, the return types, and the shared parameter names so that code written later stays coherent across all 50+ lessons.

---

## 1. Design principles

**One vocabulary everywhere.** A learner who meets `noise=`, `baseline=`, `peaks=`, and `seed=` in the UV-Vis module sees the *same* parameter names in NIR, Raman, chromatography, and sensors. The technique changes; the knobs don't. This is the single most important property for a teaching library.

**Physics in the primitives, composition in the modules.** Peak shapes, baselines, noise, and scatter live in a shared `core/` layer that knows the physics. The technique modules (`uvvis.py`, etc.) just *compose* those primitives in the way that technique demands. No physics is duplicated; fixing a peak-shape bug fixes it everywhere.

**Reproducible by construction.** Every generator takes a `seed` (or an explicit NumPy `Generator`). The same seed always yields the same data, on any machine. No global random state is ever touched.

**Beginner-friendly surface, rigorous interior.** The common case is one function call with sensible defaults: `raman.simulate()` gives a believable spectrum with zero arguments. Power users pass config objects for full control. Nothing a beginner needs is more than one keyword deep.

**Honest defaults.** Default noise, baseline, and peak parameters are chosen to look like *real* instrument output for that technique — a default NIR spectrum is scatter-dominated, a default Raman spectrum has fluorescence and a cosmic spike. Defaults teach by being realistic.

**Return data, not surprises.** Every generator returns the same lightweight `Dataset` object (described in §4). Learners destructure it the same way in every notebook.

---

## 2. Repository structure

```
python-for-analytical-chemists/
├── README.md                      # repo-level overview
├── pyproject.toml                 # package metadata, deps (numpy, scipy, pandas)
├── simulated_data/
│   ├── __init__.py                # re-exports: simulate_* and Dataset
│   ├── README.md                  # package usage (drafted separately)
│   ├── types.py                   # Dataset dataclass + helpers
│   ├── _rng.py                    # seed → Generator resolution (internal)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── axes.py                # build axis (wavelength / wavenumber / m-z / time)
│   │   ├── peaks.py               # gaussian, lorentzian, voigt, add_peaks
│   │   ├── baselines.py           # polynomial, sloping, curved, drift
│   │   ├── noise.py               # gaussian, shot/poisson, pink (1/f)
│   │   ├── scatter.py             # multiplicative + additive scatter (NIR)
│   │   ├── background.py          # broad fluorescence backgrounds (Raman)
│   │   └── artifacts.py           # cosmic-ray spikes, saturation, dropouts
│   ├── uvvis.py
│   ├── nir.py
│   ├── raman.py
│   ├── chromatography.py
│   └── sensors.py
├── notebooks/                     # the lesson notebooks (named by curriculum ID)
└── tests/
    └── test_simulated_data.py     # reproducibility + shape + sanity checks
```

The technique modules sit flat and importable (`from simulated_data import raman`). The `core/` package is the shared physics engine; lessons rarely import it directly, but advanced notebooks can.

---

## 3. Shared core primitives

These are the building blocks. Signatures shown; implementations come later.

**`core/axes.py`**
```python
build_axis(start, stop, n_points=None, step=None) -> np.ndarray
# One axis builder for all techniques. Used for nm, cm-1, m/z, minutes.
```

**`core/peaks.py`**
```python
gaussian(x, center, width, amplitude=1.0) -> np.ndarray      # width = FWHM
lorentzian(x, center, width, amplitude=1.0) -> np.ndarray
voigt(x, center, gauss_width, lorentz_width, amplitude=1.0) -> np.ndarray
add_peaks(x, peaks, shape="gaussian") -> np.ndarray
# peaks = list of (center, width, amplitude); returns summed peak profile.
```

**`core/baselines.py`**
```python
polynomial_baseline(x, coeffs, seed=None) -> np.ndarray
sloping_baseline(x, slope, offset) -> np.ndarray
curved_baseline(x, magnitude, curvature, seed=None) -> np.ndarray
# The "baseline" knob in every module routes here.
```

**`core/noise.py`**
```python
gaussian_noise(shape, level, rng) -> np.ndarray              # constant sigma
shot_noise(signal, rng) -> np.ndarray                        # Poisson, signal-dependent
pink_noise(shape, level, rng) -> np.ndarray                  # 1/f, for detector/sensor drift
# "noise" knob selects type + level; teaches that noise has structure.
```

**`core/scatter.py`**
```python
apply_scatter(X, slope_sigma, offset_sigma, rng) -> np.ndarray
# Per-sample multiplicative slope + additive offset. The physics behind SNV/MSC.
```

**`core/background.py`**
```python
fluorescence_background(x, magnitude, shape="broad", seed=None) -> np.ndarray
# Smooth broad background that dwarfs Raman peaks; the thing AsLS removes.
```

**`core/artifacts.py`**
```python
add_cosmic_rays(y, n_spikes, intensity, rng) -> np.ndarray
apply_saturation(y, ceiling) -> np.ndarray
add_dropouts(y, n, rng) -> np.ndarray
# Realistic instrument pathologies for "diagnose the bad data" lessons.
```

---

## 4. The common return type: `Dataset`

Every generator returns the same object. This is what makes notebooks feel consistent.

```python
@dataclass
class Dataset:
    x: np.ndarray            # the axis, shape (n_points,)
    X: np.ndarray            # data matrix, shape (n_samples, n_points) — always 2D
    y: np.ndarray | None     # reference values (e.g. concentrations), shape (n_samples,) or None
    meta: pd.DataFrame       # one row per sample: ids, true params, labels
    x_label: str             # "Wavelength", "Raman shift", "m/z", "Time", ...
    x_unit: str              # "nm", "cm⁻¹", "Th", "min", ...
    y_label: str             # "Absorbance", "Intensity", "Response", ...

    # convenience
    def to_frame(self) -> pd.DataFrame: ...   # wide: samples × wavelengths (+ meta)
    def single(self) -> np.ndarray: ...       # X[0] when n_samples == 1
    def plot(self, ax=None): ...              # quick look, reuses the 2.5 plotting helpers
```

Design choices that matter for teaching:
- **`X` is always 2D**, even for a single spectrum (`shape (1, n_points)`). One mental model; no special-casing. `.single()` is the beginner shortcut when there's only one sample.
- **`x` is separate from `X`** — mirrors how spectra actually are: one shared axis, many intensity vectors.
- **`meta` carries ground truth.** Because the data is simulated, `meta` can hold the *true* peak positions, concentrations, and class labels. Lessons can grade their own results against truth — a huge teaching advantage real data can't offer.
- **Labels/units travel with the data**, so plots are correct automatically.

---

## 5. The shared parameter vocabulary

Every `simulate*` function accepts this common set (technique modules add a few of their own). Keeping these names identical across modules is the contract.

| Parameter | Type | Meaning | Default behavior |
|---|---|---|---|
| `seed` | `int \| Generator \| None` | reproducibility | `None` → fresh RNG; pass an int for repeatability |
| `n_samples` | `int` | how many spectra/runs | `1` |
| `n_points` | `int` | axis resolution | technique-appropriate |
| `peaks` | `list[(center,width,amp)] \| None` | analyte bands | technique-appropriate default set |
| `peak_shape` | `str` | `"gaussian" \| "lorentzian" \| "voigt"` | technique-appropriate |
| `noise` | `float \| dict` | level, or `{type, level}` | realistic small value |
| `baseline` | `float \| dict \| None` | magnitude, or `{type, magnitude, ...}` | technique-appropriate |
| `concentration` | `float \| array \| None` | scales peak amplitudes (Beer–Lambert-like) | `1.0` |

Two access tiers, same function:
- **Beginner:** scalars. `nir.simulate(n_samples=50, noise=0.01, seed=0)`.
- **Power user:** dicts / config dataclasses. `nir.simulate(noise={"type":"pink","level":0.01}, baseline={"type":"curved","magnitude":0.3})`.

A scalar is just shorthand for the most common dict — so beginners and experts call the *same* function.

---

## 6. The five technique modules

### `uvvis.py`

**Generates:** clean, mostly-linear absorbance spectra with a few well-separated bands — the easiest technique, ideal for first lessons. Its signature feature is a **calibration series**: spectra at known concentrations following Beer–Lambert, with optional deviations (saturation, stray light) you can switch on.

**API:**
```python
simulate(peaks=None, concentration=1.0, noise=0.005, baseline=None,
         n_samples=1, seed=None, n_points=400) -> Dataset

simulate_calibration_series(concentrations, peak=(450, 40, 1.0),
                            noise=0.005, nonlinearity=0.0, seed=None) -> Dataset
#  -> Dataset with X = spectra, y = concentrations, meta has true conc + true LOD inputs.
#  nonlinearity > 0 bends Beer's law for the "when calibration fails" lesson.
```

**Example:**
```python
from simulated_data import uvvis

ds = uvvis.simulate_calibration_series(
        concentrations=[0, 2, 4, 6, 8, 10], peak=(450, 40, 0.08),
        noise=0.004, seed=0)
ds.X.shape            # (6, 400)
ds.y                  # array([0, 2, 4, 6, 8, 10])
```

**Future lessons:** 4.1 Beer–Lambert, 4.2 calibration curve + LOD, 1.4 first spectrum.

---

### `nir.py`

**Generates:** broad, overlapping NIR bands **dominated by physical scatter** — every sample gets its own multiplicative slope and additive offset (particle size, packing). This is the whole point of NIR: the chemistry is buried under scatter until you correct it. Supports a property `y` (e.g. moisture, API content) linked to band intensities for calibration lessons.

**API:**
```python
simulate(n_samples=50, peaks=None, concentration=None,
         scatter=True, baseline=None, noise=0.002, seed=None,
         n_points=700) -> Dataset

simulate_calibration_set(property_values, scatter=True, noise=0.002,
                         seed=None) -> Dataset
#  scatter can be bool or {"slope_sigma":..., "offset_sigma":...}
#  meta records each sample's true scatter slope/offset so SNV/MSC can be graded.
```

**Example:**
```python
from simulated_data import nir
ds = nir.simulate(n_samples=40, scatter={"slope_sigma":0.05,"offset_sigma":0.1}, seed=1)
# Raw X looks like spaghetti; after SNV it collapses onto the real chemistry.
```

**Future lessons:** 4.3 SNV/MSC, 4.7 preprocessing pipeline, 6.5 PLS, 6.6 validation, 6.7 calibration transfer.

---

### `raman.py`

**Generates:** sharp Lorentzian/Voigt Raman bands sitting on a **broad fluorescence background** that dwarfs them, plus optional **cosmic-ray spikes**. The two signature Raman problems are built into the defaults, so cleaning lessons have something real to clean.

**API:**
```python
simulate(peaks=None, fluorescence=1.0, cosmic_rays=2, noise=0.01,
         peak_shape="lorentzian", n_samples=1, seed=None,
         n_points=1000) -> Dataset
#  fluorescence: magnitude (0 disables). cosmic_rays: count (0 disables).
#  meta records true band positions + spike indices for grading despike/baseline.
```

**Example:**
```python
from simulated_data import raman
ds = raman.simulate(fluorescence=3.0, cosmic_rays=3, seed=7)
# A learner subtracts fluorescence (AsLS) and despikes, then checks against meta truth.
```

**Future lessons:** 4.5 Raman cleaning, 3.3 AsLS baseline, 3.4 peak detection, 4.6 spectral formats, 6.x library matching.

---

### `chromatography.py`

**Generates:** chromatograms (or generic peak trains) — Gaussian/EMG peaks on a drifting baseline, with controllable overlap, tailing, retention-time shift between runs, and noise. Supports multi-run sets for alignment and the internal-standard peak for quant lessons.

**API:**
```python
simulate(peaks=None, baseline=None, tailing=0.0, noise=0.01,
         n_samples=1, rt_shift=0.0, seed=None, n_points=2000) -> Dataset
#  tailing > 0 -> exponentially-modified Gaussian (realistic asymmetry).
#  rt_shift -> per-run retention drift for alignment lessons.

simulate_internal_standard_set(analyte_concs, is_conc=1.0,
                               noise=0.01, seed=None) -> Dataset
#  -> y = analyte concentrations; meta has true areas + IS area for response ratios.
```

**Example:**
```python
from simulated_data import chromatography as chrom
ds = chrom.simulate(peaks=[(5.0,0.1,1.0),(5.3,0.1,0.6)], tailing=0.4, seed=2)
# Overlapping, tailing peaks -> integration and deconvolution practice.
```

**Future lessons:** 3.5 integration, 3.6 deconvolution, 5.3 XIC (shares peak engine), 5.6 internal-standard quant, 5.7 run alignment.

---

### `sensors.py`

**Generates:** time-series sensor streams — a baseline with **slow drift**, embedded **step/ramp events** (the "real change" you must detect), periodic components, gaps/dropouts, and configurable noise. A multi-sensor mode produces correlated arrays for electronic-nose lessons, where each sensor has its own cross-sensitivity.

**API:**
```python
simulate(duration, sampling_rate=1.0, drift=0.0, events=None,
         noise=0.05, n_sensors=1, seed=None) -> Dataset
#  events = list of {"time":..., "type":"step|ramp|spike", "magnitude":...}
#  drift: slow baseline wander (mimics sensor aging) — distinct from events.
#  n_sensors > 1 -> X is (n_timepoints, n_sensors) array view for e-nose work.
#  x axis = time; meta records true event times + drift rate for grading.
```

**Example:**
```python
from simulated_data import sensors
ds = sensors.simulate(duration=3600, sampling_rate=1.0, drift=0.3,
                      events=[{"time":1800,"type":"step","magnitude":2.0}], seed=5)
# Learner must separate the genuine step at t=1800 from the slow drift.
```

**Future lessons:** 8.1 time-series, 8.2 drift correction, 8.3 sensor arrays / e-nose, 8.4 control charts, 8.5 predictive maintenance.

---

## 7. Reproducibility and testing

**Seed discipline.** `_rng.py` exposes one internal helper, `resolve_rng(seed)`, that turns `None`/`int`/`Generator` into a `Generator`. Every generator calls it once and threads the result through the core primitives. No function ever uses `np.random.*` global state. Consequence: `simulate(seed=0)` is byte-identical across runs and machines.

**The test suite (`tests/`) guarantees three things** every future notebook depends on:
1. *Reproducibility* — same seed → identical arrays; different seeds → different arrays.
2. *Shape contract* — `X` is always 2D, `x` length matches `X.shape[1]`, `meta` has `n_samples` rows.
3. *Scientific sanity* — peak centers land where requested; higher `concentration` gives larger area; SNV collapses NIR scatter; AsLS-able fluorescence is monotone-broad; events appear at requested times.

Because truth lives in `meta`, these sanity tests are also the templates learners reuse to grade their own analyses.

---

## 8. How this scales to 50 lessons

The leverage comes from the split: **five technique modules, one physics core, one return type, one vocabulary.** Adding a lesson almost never means new infrastructure — it means calling an existing generator with different knobs. A handful of growth paths are pre-planned:

- **New artifact to teach?** Add one function to `core/artifacts.py`; every module can opt in.
- **New technique later (e.g., MS profile spectra, XRD)?** Add `ms.py` reusing `core/peaks.py` and the `Dataset` type — no rework.
- **Real-data lessons (5.2 mzML)?** They bypass the simulators but return the *same* `Dataset`, so downstream notebooks (XIC, centroiding) don't care whether data is real or simulated. This is the bridge that lets the MS track mix real files and simulations seamlessly.

The rule for contributors: **physics goes in `core/`, technique composition goes in the module, and nothing returns anything but a `Dataset`.** Hold that line and the library stays teachable at lesson 1 and lesson 50 alike.
