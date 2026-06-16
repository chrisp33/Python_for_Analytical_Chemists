"""Raman spectroscopy -- sharp lines fighting two signature problems.

Raman is the technique where the chemistry is exquisitely specific but
practically *buried*. Two problems define it, and both are built into this
module's defaults so the cleaning lessons have something real to clean:

* **Fluorescence.** The sample re-emits absorbed laser light as a broad, smooth
  swell that is often far larger than the Raman lines themselves. It is the
  thing asymmetric-least-squares (AsLS) baseline correction removes.
* **Cosmic rays.** High-energy particles strike the detector and leave razor-
  sharp, very tall spikes that masquerade as peaks -- the classic "is that a
  peak or an artifact?" trap that despiking removes.

This module's one public entry point is :func:`simulate`. It composes the shared
``core`` primitives -- a sharp **Lorentzian** peak profile (the natural Raman
line shape), a broad **fluorescence** background, detector **noise**, and
**cosmic-ray** spikes -- into a believable raw Raman spectrum and returns the
package-wide :class:`~simulated_data.Dataset`. The *true* band positions,
fluorescence curve, and spike indices are recorded in ``meta`` so a lesson can
run AsLS + despiking and grade the result against the known answer.

The shared vocabulary
---------------------
Every knob that exists in the other technique modules means the same thing here:

* ``peaks`` -- the Raman bands, as ``(center, width, amplitude)`` triples
  (``width`` is FWHM, in cm-1); the Raman defaults are sharp Lorentzian lines;
* ``noise`` -- a level (scalar) or ``{"type": "gaussian", "level": ...}``;
* ``n_samples`` / ``n_points`` / ``seed`` -- count, resolution, reproducibility.

The two knobs unique to Raman are ``fluorescence`` (the broad background) and
``cosmic_rays`` (the spikes); see :func:`simulate`.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

from ._rng import resolve_rng
from .core.artifacts import add_cosmic_rays
from .core.axes import build_axis
from .core.background import fluorescence_background
from .core.noise import gaussian_noise
from .core.peaks import add_peaks
from .types import Dataset

__all__ = ["simulate"]

# --- Technique-appropriate defaults (the Raman "fingerprint" + C-H region). ---
_DEFAULT_START_CM = 200.0
_DEFAULT_STOP_CM = 3200.0
# (center_cm, FWHM_cm, amplitude): sharp Lorentzian lines. Amplitudes are kept
# deliberately small relative to the default fluorescence magnitude (1.0) so the
# raw spectrum is fluorescence-dominated -- the realistic Raman starting point.
_DEFAULT_PEAKS: list[tuple[float, float, float]] = [
    (620.0, 12.0, 0.30),
    (1000.0, 10.0, 0.60),   # strong, narrow ring-breathing-type line
    (1350.0, 18.0, 0.40),
    (1600.0, 16.0, 0.50),
    (2900.0, 28.0, 0.45),   # broad-ish C-H stretch region
]

# Cosmic rays are very tall by nature -- far above any real Raman line. This
# default minimum spike height dwarfs the default peak amplitudes (~0.3-0.6) and
# the default fluorescence (~1.0), so spikes are unmistakably "not chemistry".
_DEFAULT_COSMIC_INTENSITY = 5.0

# Labels that travel with the data so plots come out correct automatically.
_X_LABEL = "Raman shift"
_X_UNIT = "cm-1"
_Y_LABEL = "Intensity"


def simulate(
    peaks: Sequence[tuple[float, float, float]] | None = None,
    fluorescence: float = 1.0,
    cosmic_rays: int | dict = 2,
    noise: float | dict = 0.01,
    peak_shape: str = "lorentzian",
    n_samples: int = 1,
    seed: int | np.random.Generator | None = None,
    n_points: int = 1000,
) -> Dataset:
    """Simulate one or more raw Raman spectra, with fluorescence and spikes.

    Each spectrum is built as sharp Raman lines plus a broad fluorescence
    background plus detector noise, then has cosmic-ray spikes dropped on top::

        clean_i = (sum of Lorentzian peaks) + fluorescence_background
        noisy_i = clean_i + noise_i
        raw_i   = noisy_i with `cosmic_rays` tall spikes added at random points

    The peaks and the fluorescence curve are shared across samples (identical
    chemistry, the cleanest teaching case); what differs between rows is the
    per-sample noise and the per-sample random spike positions. The true band
    positions, the fluorescence curve, and each sample's spike indices are
    recorded in ``meta`` so a notebook can run AsLS + despiking and grade the
    recovered spectrum against the truth.

    Parameters
    ----------
    peaks : sequence of (center, width, amplitude), optional
        The Raman bands. ``center`` and ``width`` (FWHM) are in cm-1,
        ``amplitude`` is intensity at the line centre. Defaults to five sharp
        lines across the fingerprint and C-H regions.
    fluorescence : float, optional
        Peak height of the broad fluorescence background (see
        :func:`simulated_data.core.background.fluorescence_background`). ``0``
        switches fluorescence off. Defaults to ``1.0`` -- larger than the default
        peak amplitudes, so the raw spectrum is fluorescence-dominated, as real
        Raman usually is.
    cosmic_rays : int or dict, optional
        The cosmic-ray spikes. Pass an ``int`` for the count (the beginner case,
        default ``2``), or a dict for full control:
        ``{"count": n, "intensity": h}`` where ``intensity`` is the minimum
        spike height (each spike is between ``intensity`` and ``2*intensity``).
        ``0`` (or ``{"count": 0}``) switches spikes off.
    noise : float or dict, optional
        Gaussian noise level (sigma, in intensity units). A scalar, or
        ``{"type": "gaussian", "level": ...}``. Defaults to ``0.01``.
    peak_shape : str, optional
        Shape for the bands: ``"lorentzian"`` (default, the natural Raman line
        shape) or ``"gaussian"``. ``width`` is the FWHM either way.
    n_samples : int, optional
        How many spectra to generate. Defaults to ``1``. ``X`` is always 2D, so
        a single spectrum has shape ``(1, n_points)``.
    seed : int, numpy.random.Generator, or None, optional
        Reproducibility. An int gives identical data every run (use this in
        lessons); ``None`` gives fresh random data each call.
    n_points : int, optional
        Number of points on the Raman-shift axis. Defaults to ``1000`` (about
        3 cm-1 resolution over the fingerprint + C-H range).

    Returns
    -------
    Dataset
        With ``x`` = the Raman-shift axis, ``X`` = the raw spectra
        ``(n_samples, n_points)``, ``y = None``, and ``meta`` carrying the
        per-sample ground truth: a ``noise_level``, ``fluorescence`` (magnitude),
        ``n_cosmic_rays`` (count), and ``cosmic_ray_indices`` (the spiked indices
        for that sample) column. ``meta.attrs`` stores the shared truth: the base
        ``peaks``, the ``peak_shape``, the resolved ``fluorescence`` and
        ``cosmic_rays`` specs, and -- for exact grading -- the true
        ``fluorescence_curve`` and ``clean_peaks`` profiles.

    Raises
    ------
    ValueError
        If ``n_samples < 1``, for an unknown ``noise``/``peak_shape``, or for a
        malformed ``cosmic_rays`` argument.

    Examples
    --------
    A single reproducible raw spectrum -- fluorescence swell, two spikes:

    >>> ds = simulate(seed=0)
    >>> ds.X.shape
    (1, 1000)
    >>> ds.y is None
    True
    >>> len(ds.meta.attrs["fluorescence_curve"]) == ds.x.shape[0]
    True

    A stronger fluorescence and three spikes, with the spike truth recorded:

    >>> ds = simulate(fluorescence=3.0, cosmic_rays=3, seed=7)
    >>> len(ds.meta["cosmic_ray_indices"].iloc[0])
    3
    """
    if n_samples < 1:
        raise ValueError(f"n_samples must be at least 1; got {n_samples}.")

    if peaks is None:
        peaks = _DEFAULT_PEAKS

    # One generator for the whole call -> the entire dataset is reproducible
    # from the single `seed`.
    rng = resolve_rng(seed)

    # Build the shared, sample-independent pieces once: the axis, the sharp
    # Lorentzian band profile, and the broad fluorescence swell. Both the peaks
    # and the fluorescence are identical across samples (same chemistry); only
    # noise and spikes differ row-to-row.
    x = build_axis(_DEFAULT_START_CM, _DEFAULT_STOP_CM, n_points=n_points)
    clean_peaks = add_peaks(x, peaks, shape=peak_shape)        # (n_points,)
    fluor_curve = fluorescence_background(x, magnitude=fluorescence)  # (n_points,)

    clean = clean_peaks + fluor_curve                          # (n_points,)
    noise_level = _resolve_noise_level(noise)
    n_spikes, cosmic_intensity = _resolve_cosmic_rays(cosmic_rays)

    # Start every sample from the shared clean spectrum, then add per-sample
    # detector noise.
    X = np.tile(clean, (n_samples, 1))                         # (n_samples, n_points)
    X = X + gaussian_noise((n_samples, n_points), noise_level, rng)

    # Drop cosmic-ray spikes on top, per sample, recording where they landed.
    # Done after noise because a cosmic ray is a detector event sitting on top of
    # the already-measured (noisy) signal.
    spike_indices: list[np.ndarray] = []
    for i in range(n_samples):
        X[i], idx = add_cosmic_rays(X[i], n_spikes, cosmic_intensity, rng)
        spike_indices.append(idx)

    # Per-sample ground truth, plus shared truth in attrs for self-grading.
    meta = pd.DataFrame(
        {
            "noise_level": np.full(n_samples, noise_level),
            "fluorescence": np.full(n_samples, float(fluorescence)),
            "n_cosmic_rays": np.full(n_samples, n_spikes, dtype=int),
        }
    )
    # Variable-length per sample -> an object column, one index array per row.
    meta["cosmic_ray_indices"] = pd.Series(spike_indices, index=meta.index)

    meta.attrs["peaks"] = list(peaks)
    meta.attrs["peak_shape"] = peak_shape
    meta.attrs["fluorescence"] = {"magnitude": float(fluorescence), "shape": "broad"}
    meta.attrs["cosmic_rays"] = {"count": n_spikes, "intensity": cosmic_intensity}
    # The true component curves, so a lesson can grade baseline/despiking exactly.
    meta.attrs["fluorescence_curve"] = fluor_curve
    meta.attrs["clean_peaks"] = clean_peaks

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
# dict) into concrete numbers. `_resolve_noise_level` mirrors uvvis/nir exactly
# so the modules stay in lock-step; `_resolve_cosmic_rays` is unique to Raman.
# --------------------------------------------------------------------------- #


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


def _resolve_cosmic_rays(cosmic_rays: int | dict) -> tuple[int, float]:
    """Turn the ``cosmic_rays`` argument into ``(count, intensity)``.

    An ``int`` is the spike count (with the default intensity); a dict gives
    explicit control via ``{"count": ..., "intensity": ...}``, each key falling
    back to its default. ``bool`` is rejected -- ``cosmic_rays=True`` is almost
    certainly a mistake, not "one spike".
    """
    if isinstance(cosmic_rays, bool):
        raise ValueError(
            "cosmic_rays must be an int count or a dict, not a bool; "
            f"got {cosmic_rays!r}."
        )
    if isinstance(cosmic_rays, int):
        return cosmic_rays, _DEFAULT_COSMIC_INTENSITY
    if isinstance(cosmic_rays, dict):
        count = int(cosmic_rays.get("count", 0))
        intensity = float(cosmic_rays.get("intensity", _DEFAULT_COSMIC_INTENSITY))
        return count, intensity
    raise ValueError(
        "cosmic_rays must be an int count or a dict with 'count'/'intensity'; "
        f"got {cosmic_rays!r}."
    )
