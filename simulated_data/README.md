# `simulated_data`

Realistic, reproducible synthetic data for the **Python for Analytical Chemists** notebook library.

Real lab data is messy, license-restricted, and hard to share. This package generates *scientifically honest* stand-ins — UV-Vis spectra, NIR with scatter, Raman with fluorescence, chromatograms, and sensor streams — so every lesson is fully reproducible, runs offline, and ships in a public repo without data-licensing headaches.

Because the data is simulated, it carries its own ground truth. Every dataset records the *true* peak positions, concentrations, drift rates, and labels in a `meta` table — so you can grade your analysis against the real answer, something real data can never give you.

> This is a teaching tool, not a physics engine. The goal is data that *behaves* like real instrument output well enough to learn from — not a first-principles simulation.

## Install (development)

```bash
pip install -e .
```

Dependencies: `numpy`, `scipy`, `pandas`.

## Quick start

```python
from simulated_data import uvvis, nir, raman, chromatography, sensors

# One believable spectrum, zero configuration:
ds = raman.simulate(seed=0)

ds.x        # the axis (e.g. Raman shift in cm⁻¹)
ds.X        # data matrix, always 2D: (n_samples, n_points)
ds.meta     # one row per sample, with the TRUE parameters used to build it
ds.plot()   # quick look
```

Every generator returns the same `Dataset` object, so once you've learned one module you've learned them all.

## The one object you need to know: `Dataset`

| Field | What it is |
|---|---|
| `x` | the shared axis (wavelength, wavenumber, m/z, or time) |
| `X` | the data, **always 2D** — `(n_samples, n_points)`, even for one spectrum |
| `y` | reference values (e.g. concentrations), or `None` |
| `meta` | per-sample table including the **ground-truth** parameters |
| `x_label`, `x_unit`, `y_label` | labels that travel with the data so plots are correct |

Beginner shortcut: when there's only one spectrum, `ds.single()` gives you the 1D intensity vector directly.

## The knobs are the same everywhere

Learn these once; they mean the same thing in every module:

```python
seed          # int for reproducibility — same seed, same data, every time
n_samples     # how many spectra / runs to make
peaks         # list of (center, width, amplitude) for the analyte bands
noise         # noise level (scalar) or {"type": ..., "level": ...}
baseline      # baseline magnitude (scalar) or a dict for full control
concentration # scales peak amplitudes, Beer–Lambert style
```

Pass a scalar for the easy case; pass a dict when you want full control. Same function either way.

## Module map

| Module | Generates | Signature feature |
|---|---|---|
| `uvvis` | clean absorbance spectra, calibration series | Beer–Lambert; switchable nonlinearity |
| `nir` | broad overlapping bands | **scatter-dominated** — the reason SNV/MSC exist |
| `raman` | sharp bands on broad background | **fluorescence + cosmic-ray spikes** built in |
| `chromatography` | peak trains / chromatograms | tailing, overlap, retention drift, internal standard |
| `sensors` | time-series streams | slow **drift** vs embedded **events**; multi-sensor arrays |

## How notebooks should import

Always import the **module**, then call its `simulate*` function — it reads clearly in a tutorial and keeps the namespace obvious:

```python
# Recommended — clear and self-documenting in a lesson
from simulated_data import nir
ds = nir.simulate(n_samples=40, scatter=True, seed=1)
```

Avoid `from simulated_data.nir import simulate` in lessons — bare `simulate()` hides which technique it belongs to. The `Dataset` type may be imported directly when needed:

```python
from simulated_data import Dataset
```

## Reproducibility contract

Every generator takes `seed` and never touches global random state. `simulate(seed=0)` produces identical data on any machine, every run. Omit `seed` (or pass `None`) for fresh random data each call. **Lessons should always set a seed** so viewers reproduce your exact figures.

## Ground truth for self-grading

Because everything is simulated, `meta` holds the real answer. A preprocessing lesson can check its work:

```python
ds = nir.simulate(n_samples=30, scatter=True, seed=2)
true_slopes = ds.meta["scatter_slope"]      # what we secretly applied
# ... apply your SNV correction, then verify it removed the slope ...
```

This pattern — *generate with known truth, analyze, compare to `meta`* — is how the library turns every notebook into a self-checking exercise.

## Stability promise

Curriculum IDs and these public APIs are meant to stay stable as the library grows toward 50+ lessons. New techniques and artifacts are added; existing signatures and the `Dataset` shape are not broken. Internal `core/` primitives may evolve — import from the top-level modules, not from `core/`, unless a lesson is specifically about the physics.
