"""Near-infrared (NIR) spectroscopy -- the technique scatter built.

Where UV-Vis gives you clean, well-separated bands, NIR gives you the opposite:
broad, heavily **overlapping** overtone/combination bands, sitting under a thick
layer of **physical scatter**. The chemistry is real but faint; what dominates
the raw spectrum is how each sample scattered the light (particle size, packing,
texture). That is the whole pedagogical point of NIR -- the data looks like
spaghetti until you correct the scatter, and only then does the chemistry line
up.

This module's one public entry point is :func:`simulate`. It composes the shared
``core`` primitives (axis + broad peaks + baseline + noise) into a clean set of
NIR-like spectra, then -- by default -- pushes them through
:func:`simulated_data.core.scatter.apply_scatter` so every sample gets its own
multiplicative slope and additive offset. The *true* per-sample scatter is
recorded in ``meta`` so a lesson can apply SNV/MSC and grade the result against
the known answer.

Phase scope: ``simulate`` only. The property-linked calibration helper
(``simulate_calibration_set``, for the PLS lessons) is deferred to a later phase.

The shared vocabulary
---------------------
Every knob means the same thing it does in :mod:`simulated_data.uvvis`:

* ``peaks`` -- analyte bands as ``(center, width, amplitude)`` triples (``width``
  is FWHM, in nm); the NIR defaults are deliberately broad and overlapping;
* ``concentration`` -- scales band heights, Beer-Lambert style;
* ``noise`` -- a level (scalar) or ``{"type": "gaussian", "level": ...}``;
* ``baseline`` -- a magnitude (scalar), a dict, or ``None``;
* ``n_samples`` / ``n_points`` / ``seed`` -- count, resolution, reproducibility.

The one knob unique to NIR is ``scatter`` (see :func:`simulate`).
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

from ._rng import resolve_rng
from .core.axes import build_axis
from .core.baselines import curved_baseline, sloping_baseline
from .core.noise import gaussian_noise
from .core.peaks import add_peaks
from .core.scatter import apply_scatter
from .types import Dataset

__all__ = ["simulate"]

# --- Technique-appropriate defaults (short-wave/combination NIR range, nm). ---
_DEFAULT_START_NM = 1100.0
_DEFAULT_STOP_NM = 2500.0
# (center_nm, FWHM_nm, amplitude_AU): broad, overlapping NIR-like bands -- wide
# enough that neighbours blend, which is exactly how NIR overtone/combination
# bands behave (and why resolving them is hard without preprocessing).
_DEFAULT_PEAKS: list[tuple[float, float, float]] = [
    (1450.0, 120.0, 0.6),   # ~ O-H / C-H first overtone region
    (1720.0, 140.0, 0.5),   # ~ C-H first overtone
    (1940.0, 150.0, 0.8),   # ~ O-H combination (strong, broad)
    (2200.0, 200.0, 0.5),   # ~ C-H combination (very broad)
]
# Default bend for a scalar `baseline=` shorthand (a gentle, AsLS-able bow).
_DEFAULT_CURVATURE = 0.5

# Default scatter strengths for `scatter=True`. Chosen so the raw spectra fan
# out into visible "spaghetti" that SNV/MSC then collapses -- the canonical NIR
# before/after demo. (Matches the design-doc example order of magnitude.)
_DEFAULT_SLOPE_SIGMA = 0.05
_DEFAULT_OFFSET_SIGMA = 0.10

# Labels that travel with the data so plots come out correct automatically.
_X_LABEL = "Wavelength"
_X_UNIT = "nm"
_Y_LABEL = "Absorbance"


def simulate(
    n_samples: int = 50,
    peaks: Sequence[tuple[float, float, float]] | None = None,
    concentration: float | Sequence[float] | np.ndarray | None = None,
    scatter: bool | dict = True,
    baseline: float | dict | None = None,
    noise: float | dict = 0.002,
    seed: int | np.random.Generator | None = None,
    n_points: int = 700,
) -> Dataset:
    """Simulate a set of NIR absorbance spectra, with per-sample scatter.

    Each spectrum is built as broad (overlapping) bands plus an optional
    instrumental baseline, then -- unless ``scatter`` is off -- distorted by its
    own multiplicative slope and additive offset, and finally given measurement
    noise::

        clean_i      = concentration_i * (sum of broad peaks) + baseline
        scattered_i  = slope_i * clean_i + offset_i          # per-sample
        spectrum_i   = scattered_i + noise_i

    The scatter is applied to the whole clean spectrum (bands *and* baseline),
    which is physically right: scattering changes the entire measured signal, not
    just the chemistry. The true ``slope_i`` and ``offset_i`` are recorded in
    ``meta`` so a notebook can run SNV/MSC and grade the recovered chemistry
    against the known scatter.

    Parameters
    ----------
    n_samples : int, optional
        How many spectra to generate. Defaults to ``50`` -- NIR lessons are about
        *sets* of samples (the scatter only becomes visible across many spectra).
        ``X`` is always 2D, so even one sample has shape ``(1, n_points)``.
    peaks : sequence of (center, width, amplitude), optional
        The analyte bands. ``center`` and ``width`` (FWHM) are in nm, ``amplitude``
        is absorbance at unit concentration. Defaults to four broad, overlapping
        NIR-like bands.
    concentration : float, sequence of float, array, or None, optional
        Beer-Lambert scaling of band heights. A scalar applies to every sample;
        an array must have length ``n_samples``. ``None`` (default) is treated as
        ``1.0`` -- in this minimal phase every sample shares the same chemistry,
        so the *only* thing that differs between raw spectra is the scatter (the
        cleanest possible SNV/MSC demonstration). Per-sample chemistry linked to
        a property ``y`` is the job of the deferred ``simulate_calibration_set``.
    scatter : bool or dict, optional
        The per-sample physical scatter -- the heart of this module. Options:

        * ``True`` (default) -- apply scatter with sensible default strengths.
        * ``False`` -- no scatter; the clean spectra differ only by noise. Useful
          as the "after correction" target to grade against.
        * a dict -- full control: ``{"slope_sigma": ..., "offset_sigma": ...}``.
          A missing key falls back to its default strength.
    baseline : float, dict, or None, optional
        The instrumental background, identical in meaning to
        :func:`simulated_data.uvvis.simulate`:

        * ``None`` (default) -- flat zero baseline.
        * a scalar -- a gentle curved bow of that magnitude.
        * a dict -- ``{"type": "curved", "magnitude": m, "curvature": c}`` or
          ``{"type": "sloping", "slope": s, "offset": o}``.
    noise : float or dict, optional
        Gaussian noise level (sigma, in absorbance). A scalar, or
        ``{"type": "gaussian", "level": ...}``. Defaults to ``0.002`` (NIR
        detectors are quiet; scatter, not noise, is the dominant effect).
    seed : int, numpy.random.Generator, or None, optional
        Reproducibility. An int gives identical data every run (use this in
        lessons); ``None`` gives fresh random data each call.
    n_points : int, optional
        Number of points on the wavelength axis. Defaults to ``700`` (about 2 nm
        resolution over the NIR range).

    Returns
    -------
    Dataset
        With ``x`` = the wavelength axis, ``X`` = the spectra
        ``(n_samples, n_points)``, ``y = None`` (plain ``simulate`` has no target;
        the deferred calibration helper is where ``y`` is set), and ``meta``
        carrying the per-sample ground truth. ``meta`` has a ``concentration``,
        ``scatter_slope``, ``scatter_offset``, and ``noise_level`` column per
        sample, and stores the shared truth in ``meta.attrs``: the base ``peaks``,
        the resolved ``baseline`` spec, and the resolved ``scatter`` spec.

    Raises
    ------
    ValueError
        If ``n_samples < 1``, if a ``concentration`` array's length does not match
        ``n_samples``, or for an unknown ``noise``/``baseline`` type.

    Examples
    --------
    A reproducible scatter-dominated set -- raw spectra look like spaghetti:

    >>> ds = simulate(n_samples=40, scatter=True, seed=0)
    >>> ds.X.shape
    (40, 700)
    >>> ds.y is None
    True
    >>> "scatter_slope" in ds.meta.columns
    True

    Explicit scatter strengths, and the truth recorded for grading SNV/MSC:

    >>> ds = simulate(n_samples=10,
    ...               scatter={"slope_sigma": 0.05, "offset_sigma": 0.1}, seed=1)
    >>> ds.meta[["scatter_slope", "scatter_offset"]].shape
    (10, 2)
    """
    if n_samples < 1:
        raise ValueError(f"n_samples must be at least 1; got {n_samples}.")

    if peaks is None:
        peaks = _DEFAULT_PEAKS

    # One generator for the whole call -> the entire dataset is reproducible
    # from the single `seed`.
    rng = resolve_rng(seed)

    # Build the shared, concentration-independent pieces once.
    x = build_axis(_DEFAULT_START_NM, _DEFAULT_STOP_NM, n_points=n_points)
    unit_peaks = add_peaks(x, peaks)             # (n_points,)
    baseline_vec = _build_baseline(x, baseline)   # (n_points,)

    # Resolve the per-sample concentrations and the noise level.
    conc = _resolve_concentration(concentration, n_samples)   # (n_samples,)
    noise_level = _resolve_noise_level(noise)

    # Clean spectra: only the bands scale with concentration; the baseline is
    # instrumental and shared. Broadcasting (n_samples, 1) * (n_points,).
    clean = conc[:, np.newaxis] * unit_peaks[np.newaxis, :] + baseline_vec

    # Apply the per-sample physical scatter (the NIR signature). Done before
    # noise because scatter is a property of the light path, noise of the
    # detector. apply_scatter hands back the true slope/offset for `meta`.
    slope_sigma, offset_sigma = _resolve_scatter(scatter)
    scattered, scatter_slope, scatter_offset = apply_scatter(
        clean, slope_sigma, offset_sigma, rng
    )

    # Detector noise on top.
    noise_matrix = gaussian_noise((n_samples, n_points), noise_level, rng)
    X = scattered + noise_matrix

    # Per-sample ground truth, plus shared truth in attrs for self-grading.
    meta = pd.DataFrame(
        {
            "concentration": conc,
            "scatter_slope": scatter_slope,
            "scatter_offset": scatter_offset,
            "noise_level": np.full(n_samples, noise_level),
        }
    )
    meta.attrs["peaks"] = list(peaks)
    meta.attrs["baseline"] = _describe_baseline(baseline)
    meta.attrs["scatter"] = {
        "slope_sigma": slope_sigma,
        "offset_sigma": offset_sigma,
    }

    return Dataset(
        x=x,
        X=X,
        y=None,
        meta=meta,
        x_label=_X_LABEL,
        x_unit=_X_UNIT,
        y_label=_Y_LABEL,
    )


# --------------------------------------------------------------------------- #
# Internal helpers -- translators from the friendly argument forms (scalar /
# dict / bool / None) into concrete arrays and numbers. The concentration,
# noise, and baseline helpers mirror uvvis exactly so the two modules stay in
# lock-step; `_resolve_scatter` is the one piece unique to NIR.
# --------------------------------------------------------------------------- #


def _resolve_scatter(scatter: bool | dict) -> tuple[float, float]:
    """Turn the ``scatter`` argument into ``(slope_sigma, offset_sigma)``.

    ``True`` -> default strengths; ``False`` -> both zero (no scatter); a dict ->
    explicit strengths, with any missing key falling back to its default.
    """
    if scatter is True:
        return _DEFAULT_SLOPE_SIGMA, _DEFAULT_OFFSET_SIGMA
    if scatter is False:
        return 0.0, 0.0
    if isinstance(scatter, dict):
        slope_sigma = float(scatter.get("slope_sigma", _DEFAULT_SLOPE_SIGMA))
        offset_sigma = float(scatter.get("offset_sigma", _DEFAULT_OFFSET_SIGMA))
        return slope_sigma, offset_sigma
    raise ValueError(
        "scatter must be True, False, or a dict with 'slope_sigma'/"
        f"'offset_sigma'; got {scatter!r}."
    )


def _resolve_concentration(
    concentration: float | Sequence[float] | np.ndarray | None,
    n_samples: int,
) -> np.ndarray:
    """Expand the ``concentration`` argument to one value per sample.

    Accepts a scalar (broadcast to all samples), an array-like of length
    ``n_samples`` (one per sample), or ``None`` (treated as ``1.0``).
    """
    if concentration is None:
        return np.ones(n_samples)

    arr = np.atleast_1d(np.asarray(concentration, dtype=float))
    if arr.size == 1:
        return np.full(n_samples, arr.item())
    if arr.size == n_samples:
        return arr
    raise ValueError(
        "concentration must be a scalar or an array of length n_samples; "
        f"got length {arr.size} for n_samples={n_samples}."
    )


def _resolve_noise_level(noise: float | dict) -> float:
    """Turn the ``noise`` argument into a single sigma (level).

    A scalar is the level directly; a dict must be Gaussian in this phase,
    ``{"type": "gaussian", "level": ...}``.
    """
    if isinstance(noise, dict):
        noise_type = noise.get("type", "gaussian")
        if noise_type != "gaussian":
            raise ValueError(
                f"noise type {noise_type!r} is not available in this phase; "
                "only 'gaussian' is implemented."
            )
        return float(noise.get("level", 0.0))
    return float(noise)


def _build_baseline(x: np.ndarray, baseline: float | dict | None) -> np.ndarray:
    """Translate the ``baseline`` argument into a baseline array over ``x``.

    ``None`` -> flat zeros; a scalar -> a curved bow of that magnitude; a dict ->
    explicit ``"curved"`` or ``"sloping"`` baseline (see :func:`simulate`).
    """
    if baseline is None:
        return np.zeros_like(x)

    if isinstance(baseline, dict):
        b_type = baseline.get("type", "curved")
        if b_type == "curved":
            return curved_baseline(
                x,
                magnitude=baseline.get("magnitude", 0.0),
                curvature=baseline.get("curvature", _DEFAULT_CURVATURE),
            )
        if b_type == "sloping":
            return sloping_baseline(
                x,
                slope=baseline.get("slope", 0.0),
                offset=baseline.get("offset", 0.0),
            )
        raise ValueError(
            f"baseline type {b_type!r} is not recognised; use 'curved' or "
            "'sloping'."
        )

    # Scalar shorthand: a gentle curved bow of the given magnitude.
    return curved_baseline(x, magnitude=float(baseline), curvature=_DEFAULT_CURVATURE)


def _describe_baseline(baseline: float | dict | None) -> dict | None:
    """Normalise the ``baseline`` argument into a plain spec dict for ``meta``.

    Records *what baseline was actually applied* so a notebook can grade its
    baseline-correction against the truth. Returns ``None`` when no baseline was
    added.
    """
    if baseline is None:
        return None
    if isinstance(baseline, dict):
        # Copy so later mutation by the caller can't change recorded truth.
        return dict(baseline)
    return {"type": "curved", "magnitude": float(baseline), "curvature": _DEFAULT_CURVATURE}
