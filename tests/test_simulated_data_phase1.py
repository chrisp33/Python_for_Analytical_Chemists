"""Phase 1 tests for the ``simulated_data`` package.

These tests pin down the promises every future notebook relies on: the
``Dataset`` shape contract, seed reproducibility, Beer-Lambert concentration
scaling, baseline metadata, and the two ``Dataset`` conveniences
(``to_frame`` and ``single``).

They are written to be *read*, not just run -- each test checks one idea, with
a comment saying why it matters. Run them from the project root with::

    pytest

(or ``pytest tests/test_simulated_data_phase1.py`` for just this file).
"""

import numpy as np
import pytest

from simulated_data import Dataset, uvvis


def test_import_and_zero_arg_call():
    """The package imports and a no-argument call returns a Dataset.

    The friendliest possible entry point -- ``uvvis.simulate()`` with no
    arguments -- must just work and hand back the shared return type.
    """
    ds = uvvis.simulate()
    assert isinstance(ds, Dataset)


def test_dataset_shape_contract():
    """X is always 2D, the axis matches, and meta has one row per sample.

    This is the invariant every lesson destructures against, so it must hold
    even for a single spectrum (stored as shape ``(1, n_points)``).
    """
    ds = uvvis.simulate(n_samples=1, n_points=400, seed=0)
    assert ds.X.ndim == 2                       # never 1D, even for one sample
    assert ds.X.shape == (1, 400)
    assert ds.x.shape == (400,)
    assert ds.X.shape[1] == ds.x.shape[0]       # one column per axis point
    assert len(ds.meta) == ds.X.shape[0]        # one meta row per sample
    assert ds.y is None                         # plain simulate has no target


def test_same_seed_is_reproducible():
    """Same seed -> byte-identical data, so lesson figures reproduce exactly."""
    a = uvvis.simulate(seed=0)
    b = uvvis.simulate(seed=0)
    assert np.array_equal(a.X, b.X)


def test_different_seed_changes_output():
    """Different seeds -> different noise draws, so the data actually varies."""
    a = uvvis.simulate(seed=0)
    b = uvvis.simulate(seed=1)
    assert not np.array_equal(a.X, b.X)


def test_noise_zero_is_seed_independent():
    """With noise switched off, the spectrum is purely deterministic.

    ``noise=0`` draws no randomness, so the seed can't matter -- two different
    seeds must give the identical clean signal.
    """
    a = uvvis.simulate(noise=0, seed=0)
    b = uvvis.simulate(noise=0, seed=999)
    assert np.array_equal(a.X, b.X)


def test_concentration_scales_beer_lambert():
    """Doubling concentration doubles the bands (Beer-Lambert linearity).

    With no baseline and no noise, the spectrum is just the bands, so the
    relationship is exactly linear -- the core idea of UV-Vis quantitation.
    """
    one = uvvis.simulate(concentration=1.0, noise=0, baseline=None, seed=0)
    two = uvvis.simulate(concentration=2.0, noise=0, baseline=None, seed=0)
    assert two.single().sum() > one.single().sum()        # higher conc, bigger
    assert np.allclose(two.single(), 2.0 * one.single())  # and exactly 2x


def test_concentration_array_requires_matching_n_samples():
    """A concentration array must match n_samples (clear error otherwise).

    One spectrum per known concentration is the (deferred) calibration helper's
    job; plain simulate keeps n_samples explicit.
    """
    ds = uvvis.simulate(concentration=[0.5, 1.0, 1.5], n_samples=3, seed=0)
    assert list(ds.meta["concentration"]) == [0.5, 1.0, 1.5]
    with pytest.raises(ValueError):
        uvvis.simulate(concentration=[0.5, 1.0, 1.5], n_samples=2, seed=0)


def test_baseline_metadata_records_truth():
    """meta records exactly which baseline was applied, for self-grading.

    Because the data is simulated, the ground truth is stored alongside it: the
    base peaks and the resolved baseline spec live in ``meta.attrs``.
    """
    ds = uvvis.simulate(
        baseline={"type": "sloping", "slope": 0.001, "offset": 0.1}, seed=0
    )
    assert ds.meta.attrs["baseline"]["type"] == "sloping"
    assert ds.meta.attrs["baseline"]["slope"] == 0.001

    # No baseline -> recorded as None (not silently forgotten).
    clean = uvvis.simulate(baseline=None, seed=0)
    assert clean.meta.attrs["baseline"] is None

    # The true peaks are recorded too.
    assert ds.meta.attrs["peaks"] == [(450.0, 40.0, 0.8), (600.0, 60.0, 0.4)]


def test_to_frame_dimensions():
    """to_frame() returns one row per sample, with meta columns plus the axis.

    Layout: metadata columns first, then one column per axis point (labelled by
    the wavelength), indexed to match meta.
    """
    ds = uvvis.simulate(n_samples=3, n_points=400, seed=0)
    frame = ds.to_frame()
    assert frame.shape[0] == 3                       # one row per sample
    assert "concentration" in frame.columns          # meta travels along
    assert frame.shape[1] == ds.meta.shape[1] + 400  # meta cols + axis points


def test_single_returns_lone_spectrum_and_guards_multiple():
    """single() gives the 1D vector for one sample, and refuses for many.

    The beginner shortcut should never silently return "just the first" when
    there is more than one sample.
    """
    ds = uvvis.simulate(n_samples=1, n_points=400, seed=0)
    spectrum = ds.single()
    assert spectrum.shape == (400,)
    assert np.array_equal(spectrum, ds.X[0])

    many = uvvis.simulate(n_samples=2, seed=0)
    with pytest.raises(ValueError):
        many.single()
