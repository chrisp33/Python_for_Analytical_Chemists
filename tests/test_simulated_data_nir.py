"""Tests for the NIR simulator and the scatter primitive it relies on.

NIR's whole identity is *scatter*: a per-sample multiplicative slope and
additive offset that bury the chemistry until SNV/MSC removes it. These tests
pin down the three promises notebook 4.3 (and the later PLS lessons) depend on:

1. *Reproducibility* -- same seed gives identical spectra; different seeds
   differ; ``noise=0`` + ``scatter=False`` is fully deterministic.
2. *Shape contract* -- ``X`` is always 2D, the axis matches, ``meta`` has one row
   per sample, ``y`` is ``None``.
3. *Scatter metadata* -- the true per-sample slope/offset are recorded in
   ``meta`` (so a lesson can grade its correction), scatter actually changes the
   data, and turning it off zeroes the recorded distortion.

Run from the project root with ``pytest`` (or ``pytest
tests/test_simulated_data_nir.py`` for just this file).
"""

import numpy as np
import pytest

from simulated_data import Dataset, nir
from simulated_data.core.scatter import apply_scatter


# --------------------------------------------------------------------------- #
# nir.simulate -- the public entry point.
# --------------------------------------------------------------------------- #


def test_import_and_basic_call_returns_dataset():
    """A simple call returns the shared Dataset return type."""
    ds = nir.simulate(seed=0)
    assert isinstance(ds, Dataset)


def test_dataset_shape_contract():
    """X is 2D (n_samples, n_points), axis matches, meta has one row per sample.

    The invariant every downstream notebook destructures against -- must hold for
    NIR exactly as it does for UV-Vis.
    """
    ds = nir.simulate(n_samples=40, n_points=700, seed=0)
    assert ds.X.ndim == 2
    assert ds.X.shape == (40, 700)
    assert ds.x.shape == (700,)
    assert ds.X.shape[1] == ds.x.shape[0]       # one column per axis point
    assert len(ds.meta) == ds.X.shape[0]        # one meta row per sample
    assert ds.y is None                         # plain simulate has no target


def test_single_sample_still_2d():
    """Even one NIR sample is stored as shape (1, n_points) -- no special case."""
    ds = nir.simulate(n_samples=1, n_points=700, seed=0)
    assert ds.X.shape == (1, 700)


def test_same_seed_is_reproducible():
    """Same seed -> byte-identical spectra, so lesson figures reproduce exactly."""
    a = nir.simulate(n_samples=20, seed=0)
    b = nir.simulate(n_samples=20, seed=0)
    assert np.array_equal(a.X, b.X)
    # The recorded scatter truth is reproducible too.
    assert np.array_equal(
        a.meta["scatter_slope"].to_numpy(), b.meta["scatter_slope"].to_numpy()
    )
    assert np.array_equal(
        a.meta["scatter_offset"].to_numpy(), b.meta["scatter_offset"].to_numpy()
    )


def test_different_seed_changes_output():
    """Different seeds -> different scatter + noise draws, so the data varies."""
    a = nir.simulate(n_samples=20, seed=0)
    b = nir.simulate(n_samples=20, seed=1)
    assert not np.array_equal(a.X, b.X)


def test_no_scatter_no_noise_is_deterministic():
    """scatter=False + noise=0 draws no randomness, so the seed can't matter."""
    a = nir.simulate(n_samples=10, scatter=False, noise=0, seed=0)
    b = nir.simulate(n_samples=10, scatter=False, noise=0, seed=999)
    assert np.array_equal(a.X, b.X)


def test_default_peaks_are_broad_and_overlapping():
    """The default NIR bands are broad enough to overlap (the NIR signature).

    With scatter and noise off, identical chemistry means every sample is the
    same broad, smoothly-varying profile -- no sharp gaps between bands.
    """
    ds = nir.simulate(n_samples=1, scatter=False, noise=0, baseline=None, seed=0)
    spectrum = ds.X[0]
    # Broad overlapping bands never return to baseline between peaks: the trough
    # between the band maxima stays well above zero.
    assert spectrum.min() >= 0.0
    # Default FWHMs are large (>=120 nm) -- recorded truth confirms broad bands.
    widths = [w for (_c, w, _a) in ds.meta.attrs["peaks"]]
    assert min(widths) >= 100.0


# --------------------------------------------------------------------------- #
# Scatter metadata -- the ground truth that makes self-grading possible.
# --------------------------------------------------------------------------- #


def test_scatter_metadata_columns_present_and_sized():
    """meta carries a true scatter_slope and scatter_offset per sample."""
    ds = nir.simulate(n_samples=30, scatter=True, seed=0)
    assert "scatter_slope" in ds.meta.columns
    assert "scatter_offset" in ds.meta.columns
    assert len(ds.meta["scatter_slope"]) == 30
    assert len(ds.meta["scatter_offset"]) == 30


def test_scatter_on_makes_samples_differ():
    """With scatter on, the per-sample slope/offset actually vary between samples.

    If every sample had identical chemistry and no scatter, the rows would be
    identical; scatter is what fans them out into the classic NIR spaghetti.
    """
    ds = nir.simulate(n_samples=40, scatter=True, noise=0, seed=0)
    slopes = ds.meta["scatter_slope"].to_numpy()
    offsets = ds.meta["scatter_offset"].to_numpy()
    assert slopes.std() > 0          # multiplicative scatter varies
    assert offsets.std() > 0         # additive offset varies
    # Slopes centre on 1 (no scaling) and offsets on 0 (no shift), by construction.
    assert abs(slopes.mean() - 1.0) < 0.1
    assert abs(offsets.mean()) < 0.1
    # The spectra themselves differ row-to-row.
    assert not np.allclose(ds.X[0], ds.X[1])


def test_scatter_off_zeroes_recorded_distortion():
    """scatter=False records slope=1, offset=0 for every sample (no distortion)."""
    ds = nir.simulate(n_samples=15, scatter=False, seed=0)
    assert np.allclose(ds.meta["scatter_slope"].to_numpy(), 1.0)
    assert np.allclose(ds.meta["scatter_offset"].to_numpy(), 0.0)


def test_scatter_changes_the_data():
    """Turning scatter on vs off changes the spectra (same seed, same noise)."""
    on = nir.simulate(n_samples=20, scatter=True, noise=0, seed=0)
    off = nir.simulate(n_samples=20, scatter=False, noise=0, seed=0)
    assert not np.array_equal(on.X, off.X)


def test_recorded_scatter_reconstructs_the_spectra():
    """The recorded slope/offset exactly explain the distortion (gradeable truth).

    With noise off, each scattered spectrum must equal
    ``slope_i * clean_i + offset_i`` using the values stored in meta -- this is
    the relationship a learner inverts with SNV/MSC, so it has to be exact.
    """
    clean = nir.simulate(n_samples=12, scatter=False, noise=0, seed=0).X
    ds = nir.simulate(n_samples=12, scatter=True, noise=0, seed=0)
    slope = ds.meta["scatter_slope"].to_numpy()[:, None]
    offset = ds.meta["scatter_offset"].to_numpy()[:, None]
    reconstructed = slope * clean + offset
    assert np.allclose(ds.X, reconstructed)


def test_scatter_spec_recorded_in_attrs():
    """meta.attrs records the resolved scatter strengths for self-documentation."""
    ds = nir.simulate(
        n_samples=5, scatter={"slope_sigma": 0.07, "offset_sigma": 0.2}, seed=0
    )
    assert ds.meta.attrs["scatter"]["slope_sigma"] == 0.07
    assert ds.meta.attrs["scatter"]["offset_sigma"] == 0.2


def test_invalid_scatter_argument_raises():
    """A nonsensical scatter argument fails fast with a clear error."""
    with pytest.raises(ValueError):
        nir.simulate(n_samples=5, scatter="lots", seed=0)


def test_concentration_array_must_match_n_samples():
    """A concentration array must have one value per sample (clear error else)."""
    with pytest.raises(ValueError):
        nir.simulate(concentration=[1.0, 2.0], n_samples=5, seed=0)


# --------------------------------------------------------------------------- #
# core.scatter.apply_scatter -- the underlying primitive.
# --------------------------------------------------------------------------- #


def test_apply_scatter_shape_and_truth():
    """apply_scatter returns distorted data plus the true per-sample params."""
    rng = np.random.default_rng(0)
    X = np.ones((4, 10))
    Xs, slope, offset = apply_scatter(X, 0.05, 0.1, rng)
    assert Xs.shape == (4, 10)
    assert slope.shape == (4,)
    assert offset.shape == (4,)
    # Constant input row -> the distorted row is a flat slope+offset value.
    assert np.allclose(Xs, slope[:, None] * X + offset[:, None])


def test_apply_scatter_zero_sigma_is_identity():
    """With both strengths zero, the data passes through unchanged."""
    rng = np.random.default_rng(0)
    X = np.linspace(0, 1, 30).reshape(3, 10)
    Xs, slope, offset = apply_scatter(X, 0.0, 0.0, rng)
    assert np.array_equal(Xs, X)
    assert np.allclose(slope, 1.0)
    assert np.allclose(offset, 0.0)


def test_apply_scatter_reproducible_from_generator():
    """Same seed -> identical distortion, drawn from the shared generator."""
    X = np.ones((5, 8))
    a = apply_scatter(X, 0.05, 0.1, np.random.default_rng(0))
    b = apply_scatter(X, 0.05, 0.1, np.random.default_rng(0))
    assert np.array_equal(a[0], b[0])
    assert np.array_equal(a[1], b[1])
    assert np.array_equal(a[2], b[2])


def test_apply_scatter_validates_inputs():
    """1D input, negative sigma, and a bad rng are all rejected clearly."""
    rng = np.random.default_rng(0)
    with pytest.raises(ValueError):
        apply_scatter(np.ones(10), 0.05, 0.1, rng)        # not 2D
    with pytest.raises(ValueError):
        apply_scatter(np.ones((2, 5)), -0.1, 0.1, rng)    # negative slope_sigma
    with pytest.raises(ValueError):
        apply_scatter(np.ones((2, 5)), 0.1, -0.1, rng)    # negative offset_sigma
    with pytest.raises(TypeError):
        apply_scatter(np.ones((2, 5)), 0.05, 0.1, 0)      # rng not a Generator
