"""Peak shapes -- the bands that ride on top of a spectrum.

Almost every analytical signal is "peaks on a background": absorbance bands,
Raman lines, chromatographic peaks. This module builds the peaks. Two shapes
are implemented:

* **Gaussian** -- the right default for UV-Vis bands and the easiest shape to
  reason about;
* **Lorentzian** -- the natural shape of a Raman line (and many spectroscopic
  transitions), sharper at the top and with **heavier tails** than a Gaussian
  of the same width.

The Voigt shape (a Gaussian/Lorentzian convolution, for instrument-broadened
lines) is still deferred.

A key teaching choice: **width is the FWHM** -- the full width at half maximum,
the width of the peak measured halfway up. That's the number a chemist actually
reads off a spectrum, far more intuitive than the Gaussian's internal ``sigma``
or the Lorentzian's half-width ``gamma``. This module does the conversion for
you, so the *same* ``width`` argument means the same measured width for either
shape.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

__all__ = ["gaussian", "lorentzian", "add_peaks"]

# Convert a Gaussian's FWHM to its standard deviation (sigma).
#
#   FWHM = 2 * sqrt(2 * ln 2) * sigma   ->   sigma = FWHM / (2 sqrt(2 ln 2))
#
# We expose `width` as FWHM (what you measure on a plot) and convert internally,
# so callers never have to think about sigma.
_FWHM_TO_SIGMA = 1.0 / (2.0 * np.sqrt(2.0 * np.log(2.0)))


def gaussian(
    x: np.ndarray,
    center: float,
    width: float,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Evaluate a single Gaussian peak on the axis ``x``.

    The peak's height at its centre equals ``amplitude``, and its full width at
    half maximum equals ``width``. Formally::

        y = amplitude * exp(-(x - center)**2 / (2 * sigma**2))

    where ``sigma`` is derived from ``width`` (the FWHM).

    Parameters
    ----------
    x : numpy.ndarray
        The axis to evaluate on, shape ``(n_points,)`` (e.g. from
        :func:`simulated_data.core.axes.build_axis`).
    center : float
        Position of the peak maximum, in the units of ``x``.
    width : float
        Full width at half maximum (FWHM), in the units of ``x``. Must be
        positive. A larger FWHM is a broader band.
    amplitude : float, optional
        Peak height at ``center``. Defaults to ``1.0``. Positive for a normal
        absorbance/intensity band; negative would model a dip.

    Returns
    -------
    numpy.ndarray
        The peak profile, same shape as ``x``.

    Raises
    ------
    ValueError
        If ``width`` is not positive.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.linspace(0, 10, 11)
    >>> y = gaussian(x, center=5, width=2, amplitude=3.0)
    >>> float(y.max())          # height at the centre equals the amplitude
    3.0
    >>> int(y.argmax())         # peak sits at x = 5 (index 5)
    5
    """
    if width <= 0:
        raise ValueError(f"width (FWHM) must be positive; got {width}.")

    x = np.asarray(x, dtype=float)
    sigma = width * _FWHM_TO_SIGMA
    return amplitude * np.exp(-((x - center) ** 2) / (2.0 * sigma**2))


def lorentzian(
    x: np.ndarray,
    center: float,
    width: float,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Evaluate a single Lorentzian peak on the axis ``x``.

    The peak's height at its centre equals ``amplitude``, and its full width at
    half maximum equals ``width``. Formally::

        y = amplitude * gamma**2 / ((x - center)**2 + gamma**2)

    where ``gamma = width / 2`` is the half-width at half-maximum (so the value
    at ``center +/- gamma`` is exactly ``amplitude / 2``, i.e. FWHM = ``width``).

    Compared with a Gaussian of the same ``width``, a Lorentzian is more sharply
    peaked at the top and has much **heavier tails** -- it returns to baseline
    slowly. That is the characteristic shape of a Raman line, which is why this
    is the default peak shape for :mod:`simulated_data.raman`.

    Parameters
    ----------
    x : numpy.ndarray
        The axis to evaluate on, shape ``(n_points,)`` (e.g. from
        :func:`simulated_data.core.axes.build_axis`).
    center : float
        Position of the peak maximum, in the units of ``x``.
    width : float
        Full width at half maximum (FWHM), in the units of ``x``. Must be
        positive. A larger FWHM is a broader band.
    amplitude : float, optional
        Peak height at ``center``. Defaults to ``1.0``. Positive for a normal
        intensity band; negative would model a dip.

    Returns
    -------
    numpy.ndarray
        The peak profile, same shape as ``x``.

    Raises
    ------
    ValueError
        If ``width`` is not positive.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.linspace(0, 10, 11)
    >>> y = lorentzian(x, center=5, width=2, amplitude=3.0)
    >>> float(y.max())          # height at the centre equals the amplitude
    3.0
    >>> int(y.argmax())         # peak sits at x = 5 (index 5)
    5
    >>> float(lorentzian(np.array([6.0]), center=5, width=2)[0])  # at center+gamma
    0.5
    """
    if width <= 0:
        raise ValueError(f"width (FWHM) must be positive; got {width}.")

    x = np.asarray(x, dtype=float)
    gamma = width / 2.0
    return amplitude * gamma**2 / ((x - center) ** 2 + gamma**2)


# Dispatch table: a shape name -> the single-peak function that draws it. Adding
# a new shape later (e.g. "voigt") means adding one entry here.
_PEAK_SHAPES = {
    "gaussian": gaussian,
    "lorentzian": lorentzian,
}


def add_peaks(
    x: np.ndarray,
    peaks: Sequence[tuple[float, float, float]],
    shape: str = "gaussian",
) -> np.ndarray:
    """Sum several peaks into one profile.

    Real spectra are several bands added together, so this helper takes a list
    of peak specs and returns their sum on the shared axis ``x``. Overlapping
    peaks simply add, which is exactly how convoluted/unresolved bands arise --
    useful for peak-detection and deconvolution lessons.

    Parameters
    ----------
    x : numpy.ndarray
        The axis to evaluate on, shape ``(n_points,)``.
    peaks : sequence of (center, width, amplitude)
        One tuple per peak: its centre, FWHM, and height (see :func:`gaussian`).
        An empty sequence returns an all-zero profile.
    shape : str, optional
        Peak shape to use for every peak: ``"gaussian"`` (default, for UV-Vis /
        NIR bands) or ``"lorentzian"`` (for Raman lines). ``width`` is the FWHM
        in both cases, so the same spec gives the same measured width whichever
        shape you choose. (``"voigt"`` is not yet implemented.)

    Returns
    -------
    numpy.ndarray
        The summed profile, same shape as ``x``.

    Raises
    ------
    ValueError
        If ``shape`` is not a recognised peak shape, or if any peak spec does
        not have exactly three values ``(center, width, amplitude)``.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.linspace(400, 500, 101)
    >>> y = add_peaks(x, [(430, 10, 1.0), (470, 10, 0.5)])
    >>> y.shape
    (101,)

    The same spec drawn as sharp Lorentzian lines (e.g. for Raman):

    >>> y = add_peaks(x, [(430, 10, 1.0), (470, 10, 0.5)], shape="lorentzian")
    >>> y.shape
    (101,)
    """
    try:
        peak_fn = _PEAK_SHAPES[shape]
    except KeyError:
        available = ", ".join(repr(s) for s in _PEAK_SHAPES)
        raise ValueError(
            f"shape={shape!r} is not recognised; available shapes are "
            f"{available}. ('voigt' is not yet implemented.)"
        ) from None

    x = np.asarray(x, dtype=float)
    # Start from a flat zero profile and add each peak onto it.
    profile = np.zeros_like(x)
    for i, peak in enumerate(peaks):
        if len(peak) != 3:
            raise ValueError(
                "each peak must be a (center, width, amplitude) triple; "
                f"peak at index {i} has {len(peak)} value(s): {peak!r}."
            )
        center, width, amplitude = peak
        profile += peak_fn(x, center, width, amplitude)
    return profile
