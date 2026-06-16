"""UV-Vis spectroscopy -- the workhorse technique for the early lessons.

UV-Visible absorbance is the gentlest place to start: a few well-separated bands
on a mostly-flat background, with absorbance proportional to concentration
(Beer-Lambert). That clean behaviour is exactly why it carries the first run of
notebooks -- reading/writing files, plotting, smoothing, baseline correction.

This module's one public entry point is :func:`simulate`, which composes the
shared ``core`` primitives (axis + peaks + baseline + noise) into a believable
absorbance spectrum and returns the package-wide :class:`~simulated_data.Dataset`.

Phase 1 scope: ``simulate`` only. The calibration-series helper
(``simulate_calibration_series``) and nonlinearity/saturation switches are
deferred to a later phase.

The shared vocabulary
---------------------
Every knob here means the same thing it will mean in the other technique
modules:

* ``peaks`` -- the analyte bands, as ``(center, width, amplitude)`` triples
  (``width`` is FWHM, in nm);
* ``concentration`` -- scales band heights, Beer-Lambert style;
* ``noise`` -- a level (scalar) or ``{"type": "gaussian", "level": ...}``;
* ``baseline`` -- a magnitude (scalar) or a dict for full control, or ``None``;
* ``n_samples`` / ``n_points`` / ``seed`` -- count, resolution, reproducibility.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

from ._rng import resolve_rng
from .core.baselines import curved_baseline, sloping_baseline
from .core.noise import gaussian_noise
from .core.peaks import add_peaks
from .core.axes import build_axis
from .types import Dataset

__all__ = ["simulate"]

# --- Technique-appropriate defaults (visible range, two well-separated bands). ---
_DEFAULT_START_NM = 400.0
_DEFAULT_STOP_NM = 800.0
# (center_nm, FWHM_nm, amplitude_AU): two clean, non-overlapping absorbance bands.
_DEFAULT_PEAKS: list[tuple[float, float, float]] = [
    (450.0, 40.0, 0.8),
    (600.0, 60.0, 0.4),
]
# Default bend for a scalar `baseline=` shorthand (a gentle, AsLS-able bow).
_DEFAULT_CURVATURE = 0.5

# Labels that travel with the data so plots come out correct automatically.
_X_LABEL = "Wavelength"
_X_UNIT = "nm"
_Y_LABEL = "Absorbance"


def simulate(
    peaks: Sequence[tuple[float, float, float]] | None = None,
    concentration: float | Sequence[float] | np.ndarray | None = 1.0,
    noise: float | dict = 0.005,
    baseline: float | dict | None = None,
    n_samples: int = 1,
    seed: int | np.random.Generator | None = None,
    n_points: int = 400,
) -> Dataset:
    """Simulate one or more UV-Vis absorbance spectra.

    Each spectrum is built as Beer-Lambert bands plus an optional baseline plus
    measurement noise::

        spectrum_i = concentration_i * (sum of peaks) + baseline + noise_i

    The baseline and the noise model the *instrument*, so the baseline does not
    scale with concentration (only the analyte bands do) -- which is what makes
    this a faithful Beer-Lambert teaching example.

    Parameters
    ----------
    peaks : sequence of (center, width, amplitude), optional
        The analyte bands. ``center`` and ``width`` (FWHM) are in nm,
        ``amplitude`` is absorbance at unit concentration. Defaults to two
        well-separated visible bands.
    concentration : float, sequence of float, array, or None, optional
        Beer-Lambert scaling of band heights. A scalar applies to every sample;
        an array must have length ``n_samples`` (one concentration per
        spectrum). ``None`` is treated as ``1.0``. Defaults to ``1.0``.
    noise : float or dict, optional
        Gaussian noise level (sigma, in absorbance). Pass a scalar for the easy
        case, or ``{"type": "gaussian", "level": ...}`` for the explicit form.
        ``0`` gives a noise-free spectrum. Defaults to ``0.005``.
    baseline : float, dict, or None, optional
        The instrumental background. Options:

        * ``None`` (default) -- flat zero baseline.
        * a scalar -- shorthand for a gentle curved bow of that magnitude
          (``{"type": "curved", "magnitude": <scalar>}``).
        * a dict -- full control. ``{"type": "curved", "magnitude": m,
          "curvature": c}`` or ``{"type": "sloping", "slope": s, "offset": o}``.
    n_samples : int, optional
        How many spectra to generate. Defaults to ``1``. ``X`` is always 2D, so
        a single spectrum has shape ``(1, n_points)``.
    seed : int, numpy.random.Generator, or None, optional
        Reproducibility. An int gives identical data every run (use this in
        lessons); ``None`` gives fresh random data each call. See
        :func:`simulated_data._rng.resolve_rng`.
    n_points : int, optional
        Number of points on the wavelength axis. Defaults to ``400`` (about
        1 nm resolution over the visible range).

    Returns
    -------
    Dataset
        With ``x`` = the wavelength axis, ``X`` = the spectra
        ``(n_samples, n_points)``, ``y = None`` (plain ``simulate`` has no
        target; the calibration helper, deferred, is where ``y`` is set), and
        ``meta`` carrying the per-sample ground truth. ``meta`` has a
        ``concentration`` and ``noise_level`` column per sample, and stores the
        shared truth in ``meta.attrs``: the base ``peaks`` and the resolved
        ``baseline`` spec -- so a lesson can grade its analysis against what was
        actually used.

    Raises
    ------
    ValueError
        If ``n_samples < 1``, or if a ``concentration`` array's length does not
        match ``n_samples``, or for an unknown ``noise``/``baseline`` type.

    Examples
    --------
    A single reproducible spectrum:

    >>> ds = simulate(seed=0)
    >>> ds.X.shape
    (1, 400)
    >>> ds.y is None
    True

    A small batch at different concentrations, with a curved baseline. Pass
    ``n_samples`` to match the number of concentrations -- a length mismatch is
    rejected (one spectrum per known concentration is the job of the deferred
    calibration helper):

    >>> ds = simulate(concentration=[0.5, 1.0, 1.5], n_samples=3,
    ...               baseline=0.2, seed=0)
    >>> ds.X.shape
    (3, 400)
    >>> list(ds.meta["concentration"])
    [0.5, 1.0, 1.5]
    """
    if n_samples < 1:
        raise ValueError(f"n_samples must be at least 1; got {n_samples}.")

    if peaks is None:
        peaks = _DEFAULT_PEAKS

    # One generator for the whole call -> the entire dataset is reproducible
    # from the single `seed`.
    rng = resolve_rng(seed)

    # Build the shared pieces once: the axis, the unit-concentration band shape,
    # and the (concentration-independent) instrumental baseline.
    x = build_axis(_DEFAULT_START_NM, _DEFAULT_STOP_NM, n_points=n_points)
    unit_peaks = add_peaks(x, peaks)            # shape (n_points,)
    baseline_vec = _build_baseline(x, baseline)  # shape (n_points,)

    # Resolve the per-sample concentrations and the noise level.
    conc = _resolve_concentration(concentration, n_samples)   # (n_samples,)
    noise_level = _resolve_noise_level(noise)

    # Compose the data matrix. Beer-Lambert: only the bands scale with
    # concentration; the baseline is instrumental and shared by all samples.
    # Broadcasting: (n_samples, 1) * (n_points,) -> (n_samples, n_points).
    signal = conc[:, np.newaxis] * unit_peaks[np.newaxis, :] + baseline_vec
    noise_matrix = gaussian_noise((n_samples, n_points), noise_level, rng)
    X = signal + noise_matrix

    # Per-sample ground truth, plus shared truth in attrs for self-grading.
    meta = pd.DataFrame(
        {
            "concentration": conc,
            "noise_level": np.full(n_samples, noise_level),
        }
    )
    meta.attrs["peaks"] = list(peaks)
    meta.attrs["baseline"] = _describe_baseline(baseline)

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
# Internal helpers -- small, single-purpose translators from the friendly
# argument forms (scalar / dict / None) into concrete arrays and numbers.
# --------------------------------------------------------------------------- #


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
