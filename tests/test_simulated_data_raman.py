"""Tests for the Raman simulator and the primitives it adds.

Raman's identity is two signature problems layered over sharp lines: a broad
**fluorescence** background that dwarfs the peaks, and **cosmic-ray** spikes that
masquerade as peaks. These tests pin down the promises notebook 4.5 (cosmic-ray
removal + fluorescence baselines) depends on:

1. *The Lorentzian line shape* -- correct FWHM, correct height, heavier tails
   than a Gaussian (so it reads as a Raman line).
2. *The fluorescence background* -- broad, smooth, peak equal to its magnitude,
   switchable off.
3. *Cosmic rays* -- the right number of tall spikes at recorded indices,
   reproducible, switchable off without disturbing the RNG stream.
4. *raman.simulate* -- reproducibility, the shape contract, fluorescence that
   dominates the peaks, and ground-truth metadata (band positions, the true
   fluorescence curve, and per-sample spike indices) for self-grading.

Run from the project root with ``pytest`` (or ``pytest
tests/test_simulated_data_raman.py`` for just this file).
"""

import numpy as np
import pytest

from simulated_data import Dataset, raman
from simulated_data.core.artifacts import add_cosmic_rays
from simulated_data.core.background import fluorescence_background
from simulated_data.core.peaks import add_peaks, gaussian, lorentzian


# --------------------------------------------------------------------------- #
# core.peaks.lorentzian -- the natural Raman line shape.
# --------------------------------------------------------------------------- #


def test_lorentzian_height_and_center():
    """Height at the centre equals amplitude, and the max sits at center."""
    x = np.linspace(0, 10, 1001)
    y = lorentzian(x, center=5.0, width=2.0, amplitude=3.0)
    assert np.isclose(y.max(), 3.0)
    assert np.isclose(x[y.argmax()], 5.0, atol=1e-2)


def test_lorentzian_fwhm_is_width():
    """The value at center +/- width/2 is exactly half the amplitude (FWHM=width)."""
    x = np.array([4.0, 5.0, 6.0])           # center=5, width=2 -> gamma=1
    y = lorentzian(x, center=5.0, width=2.0, amplitude=1.0)
    assert np.isclose(y[0], 0.5)            # at center - gamma
    assert np.isclose(y[2], 0.5)            # at center + gamma


def test_lorentzian_has_heavier_tails_than_gaussian():
    """Far from the centre a Lorentzian sits well above a same-width Gaussian.

    The heavy tail is what makes a Lorentzian read as a Raman line rather than a
    rounded UV-Vis band -- it returns to baseline slowly.
    """
    x = np.array([20.0])                     # far from center=0 vs width=2
    lor = lorentzian(x, center=0.0, width=2.0, amplitude=1.0)[0]
    gau = gaussian(x, center=0.0, width=2.0, amplitude=1.0)[0]
    assert lor > gau


def test_lorentzian_rejects_nonpositive_width():
    """A zero or negative FWHM is meaningless and fails fast."""
    x = np.linspace(0, 10, 11)
    with pytest.raises(ValueError):
        lorentzian(x, center=5.0, width=0.0)


def test_add_peaks_supports_lorentzian_and_rejects_unknown():
    """add_peaks can draw Lorentzian lines; an unimplemented shape errors."""
    x = np.linspace(0, 100, 501)
    prof = add_peaks(x, [(30.0, 5.0, 1.0), (70.0, 5.0, 0.5)], shape="lorentzian")
    assert prof.shape == x.shape
    assert prof.max() > 0
    with pytest.raises(ValueError):
        add_peaks(x, [(30.0, 5.0, 1.0)], shape="voigt")


# --------------------------------------------------------------------------- #
# core.background.fluorescence_background -- the broad swell AsLS removes.
# --------------------------------------------------------------------------- #


def test_fluorescence_peak_equals_magnitude_and_nonnegative():
    """The background's maximum equals the requested magnitude, and it's >= 0."""
    x = np.linspace(200, 3200, 1000)
    bg = fluorescence_background(x, magnitude=3.0)
    assert np.isclose(bg.max(), 3.0)
    assert (bg >= 0).all()
    assert bg.shape == x.shape


def test_fluorescence_is_broad_and_smooth():
    """The background varies slowly -- no sharp features for despiking to catch.

    A broad, smooth curve has a tiny point-to-point change relative to its
    overall size; that smoothness is exactly what makes it AsLS-removable and
    distinct from the sharp Raman lines and cosmic rays.
    """
    x = np.linspace(200, 3200, 1000)
    bg = fluorescence_background(x, magnitude=1.0)
    step_changes = np.abs(np.diff(bg))
    # Each step is a minuscule fraction of the full background height.
    assert step_changes.max() < 0.01 * bg.max()


def test_fluorescence_zero_magnitude_is_off():
    """magnitude=0 returns a flat zero background (fluorescence switched off)."""
    x = np.linspace(200, 3200, 1000)
    assert np.array_equal(fluorescence_background(x, magnitude=0.0), np.zeros_like(x))


def test_fluorescence_is_deterministic():
    """Same inputs -> identical curve (the background carries no randomness)."""
    x = np.linspace(200, 3200, 1000)
    assert np.array_equal(
        fluorescence_background(x, magnitude=2.0),
        fluorescence_background(x, magnitude=2.0),
    )


def test_fluorescence_rejects_negative_and_unknown_shape():
    """Negative magnitude and an unknown shape both fail fast."""
    x = np.linspace(200, 3200, 1000)
    with pytest.raises(ValueError):
        fluorescence_background(x, magnitude=-1.0)
    with pytest.raises(ValueError):
        fluorescence_background(x, magnitude=1.0, shape="sloping")


# --------------------------------------------------------------------------- #
# core.artifacts.add_cosmic_rays -- spikes plus the ground truth.
# --------------------------------------------------------------------------- #


def test_add_cosmic_rays_count_and_truth():
    """The right number of distinct spikes are added, each at least `intensity`."""
    rng = np.random.default_rng(0)
    y = np.zeros(200)
    y_spiked, idx = add_cosmic_rays(y, n_spikes=4, intensity=5.0, rng=rng)
    assert idx.shape == (4,)
    assert len(set(idx.tolist())) == 4              # distinct positions
    assert (y_spiked[idx] >= 5.0).all()             # each spike is tall
    assert np.array_equal(np.sort(idx), idx)        # returned sorted


def test_add_cosmic_rays_does_not_mutate_input():
    """The input spectrum is left untouched; a copy is returned."""
    rng = np.random.default_rng(0)
    y = np.zeros(50)
    add_cosmic_rays(y, n_spikes=3, intensity=5.0, rng=rng)
    assert np.array_equal(y, np.zeros(50))


def test_add_cosmic_rays_zero_is_noop_and_draws_nothing():
    """n_spikes=0 returns an unchanged copy and does not disturb the RNG stream.

    Disabling spikes must not shift later random draws -- so a downstream noise
    draw is identical whether or not spikes were 'added'.
    """
    y = np.zeros(50)
    rng_a = np.random.default_rng(0)
    out, idx = add_cosmic_rays(y, n_spikes=0, intensity=5.0, rng=rng_a)
    assert np.array_equal(out, y)
    assert idx.size == 0
    # The generator is untouched: its next draw matches a fresh, undrawn one.
    rng_b = np.random.default_rng(0)
    assert np.array_equal(rng_a.random(5), rng_b.random(5))


def test_add_cosmic_rays_reproducible():
    """Same seed -> identical spikes and identical indices."""
    y = np.zeros(100)
    a_y, a_idx = add_cosmic_rays(y, 3, 5.0, np.random.default_rng(0))
    b_y, b_idx = add_cosmic_rays(y, 3, 5.0, np.random.default_rng(0))
    assert np.array_equal(a_y, b_y)
    assert np.array_equal(a_idx, b_idx)


def test_add_cosmic_rays_validates_inputs():
    """2D input, too many spikes, negative intensity, bad rng all rejected."""
    rng = np.random.default_rng(0)
    with pytest.raises(ValueError):
        add_cosmic_rays(np.zeros((2, 5)), 1, 5.0, rng)        # not 1D
    with pytest.raises(ValueError):
        add_cosmic_rays(np.zeros(5), 6, 5.0, rng)             # more spikes than points
    with pytest.raises(ValueError):
        add_cosmic_rays(np.zeros(5), 1, -1.0, rng)            # negative intensity
    with pytest.raises(TypeError):
        add_cosmic_rays(np.zeros(5), 1, 5.0, 0)               # rng not a Generator


# --------------------------------------------------------------------------- #
# raman.simulate -- the public entry point.
# --------------------------------------------------------------------------- #


def test_import_and_basic_call_returns_dataset():
    """A simple call returns the shared Dataset return type."""
    ds = raman.simulate(seed=0)
    assert isinstance(ds, Dataset)


def test_dataset_shape_contract():
    """X is 2D (n_samples, n_points), axis matches, meta has one row per sample."""
    ds = raman.simulate(n_samples=5, n_points=1000, seed=0)
    assert ds.X.ndim == 2
    assert ds.X.shape == (5, 1000)
    assert ds.x.shape == (1000,)
    assert ds.X.shape[1] == ds.x.shape[0]
    assert len(ds.meta) == ds.X.shape[0]
    assert ds.y is None


def test_single_sample_still_2d():
    """Even one Raman sample is stored as shape (1, n_points)."""
    ds = raman.simulate(n_samples=1, n_points=1000, seed=0)
    assert ds.X.shape == (1, 1000)
    assert ds.single().shape == (1000,)


def test_same_seed_is_reproducible():
    """Same seed -> byte-identical spectra and identical spike locations."""
    a = raman.simulate(n_samples=4, seed=0)
    b = raman.simulate(n_samples=4, seed=0)
    assert np.array_equal(a.X, b.X)
    for ia, ib in zip(a.meta["cosmic_ray_indices"], b.meta["cosmic_ray_indices"]):
        assert np.array_equal(ia, ib)


def test_different_seed_changes_output():
    """Different seeds -> different noise and spike draws, so the data varies."""
    a = raman.simulate(n_samples=4, seed=0)
    b = raman.simulate(n_samples=4, seed=1)
    assert not np.array_equal(a.X, b.X)


def test_no_noise_no_fluorescence_no_spikes_is_deterministic():
    """With every random/added effect off, the seed cannot matter."""
    a = raman.simulate(n_samples=3, fluorescence=0, cosmic_rays=0, noise=0, seed=0)
    b = raman.simulate(n_samples=3, fluorescence=0, cosmic_rays=0, noise=0, seed=9)
    assert np.array_equal(a.X, b.X)


def test_default_fluorescence_dominates_peaks():
    """By default the broad fluorescence is the largest non-spike feature.

    With spikes and noise off, the raw spectrum's bulk is the fluorescence swell
    (magnitude 1.0), which sits well above the sharp peaks (amplitudes ~0.3-0.6)
    -- the realistic 'chemistry buried under fluorescence' starting point.
    """
    ds = raman.simulate(n_samples=1, cosmic_rays=0, noise=0, seed=0)
    fluor = ds.meta.attrs["fluorescence_curve"]
    clean_peaks = ds.meta.attrs["clean_peaks"]
    assert fluor.max() > clean_peaks.max()


def test_meta_columns_present():
    """meta carries the per-sample ground truth columns 4.5 needs."""
    ds = raman.simulate(n_samples=3, cosmic_rays=2, seed=0)
    for col in ("noise_level", "fluorescence", "n_cosmic_rays", "cosmic_ray_indices"):
        assert col in ds.meta.columns
    assert (ds.meta["n_cosmic_rays"] == 2).all()


def test_cosmic_ray_indices_match_actual_spikes():
    """The recorded indices are exactly where the raw spectrum spikes upward.

    A learner despikes and compares against these indices, so they must point at
    the real spikes. Compared to the clean (no-spike) spectrum at the same seed,
    the raw spectrum must be much higher exactly at the recorded indices.
    """
    raw = raman.simulate(n_samples=1, cosmic_rays=3, noise=0.01, seed=0)
    clean = raman.simulate(n_samples=1, cosmic_rays=0, noise=0.01, seed=0)
    idx = raw.meta["cosmic_ray_indices"].iloc[0]
    assert len(idx) == 3
    # At the spiked points the raw spectrum towers over the (un-spiked) baseline.
    bumps = raw.X[0][idx] - clean.X[0][idx]
    assert (bumps >= _DEFAULT_MIN_SPIKE).all()


def test_cosmic_rays_off_records_no_spikes():
    """cosmic_rays=0 yields empty spike-index arrays and a zero count."""
    ds = raman.simulate(n_samples=2, cosmic_rays=0, seed=0)
    assert (ds.meta["n_cosmic_rays"] == 0).all()
    for idx in ds.meta["cosmic_ray_indices"]:
        assert len(idx) == 0


def test_cosmic_rays_dict_controls_count_and_intensity():
    """A dict cosmic_rays argument sets both the count and the spike intensity."""
    ds = raman.simulate(
        n_samples=1, cosmic_rays={"count": 4, "intensity": 12.0}, noise=0, seed=0
    )
    assert ds.meta.attrs["cosmic_rays"] == {"count": 4, "intensity": 12.0}
    idx = ds.meta["cosmic_ray_indices"].iloc[0]
    assert len(idx) == 4
    # Each spike is at least the requested intensity above the local baseline.
    clean = raman.simulate(n_samples=1, cosmic_rays=0, noise=0, seed=0)
    assert (ds.X[0][idx] - clean.X[0][idx] >= 12.0).all()


def test_attrs_record_shared_truth():
    """meta.attrs records peaks, shape, fluorescence, and the true curves."""
    ds = raman.simulate(n_samples=1, fluorescence=2.0, seed=0)
    assert ds.meta.attrs["peak_shape"] == "lorentzian"
    assert ds.meta.attrs["fluorescence"]["magnitude"] == 2.0
    assert len(ds.meta.attrs["peaks"]) == 5
    assert ds.meta.attrs["fluorescence_curve"].shape == ds.x.shape
    assert ds.meta.attrs["clean_peaks"].shape == ds.x.shape


def test_invalid_peak_shape_raises():
    """An unimplemented peak shape fails fast with a clear error."""
    with pytest.raises(ValueError):
        raman.simulate(peak_shape="voigt", seed=0)


def test_invalid_cosmic_rays_argument_raises():
    """A nonsensical cosmic_rays argument (incl. bool) fails fast."""
    with pytest.raises(ValueError):
        raman.simulate(cosmic_rays="lots", seed=0)
    with pytest.raises(ValueError):
        raman.simulate(cosmic_rays=True, seed=0)


# The default minimum cosmic-ray spike height (mirrors raman._DEFAULT_COSMIC_INTENSITY);
# spikes are between this and twice this above the local signal.
_DEFAULT_MIN_SPIKE = 5.0
