"""Broad backgrounds -- the slow swell a spectrum can sit on top of.

This is the Raman counterpart to :mod:`simulated_data.core.baselines`. Where a
UV-Vis baseline is a gentle tilt or bow, a Raman spectrum's background is
**fluorescence**: the sample (or its impurities) absorbs the laser and
re-emits light as a broad, smooth swell that is often *far larger* than the
sharp Raman lines riding on it. The whole difficulty of Raman -- and the reason
asymmetric-least-squares (AsLS) baseline correction matters so much there -- is
that the chemistry you want is a small ripple on top of a big, slow hump.

To *teach* removing that hump you first need data that has a realistic one, and
that is what :func:`fluorescence_background` makes: a broad, smooth curve scaled
so its peak equals a chosen ``magnitude``, returned as an array meant to be
*added* to a clean (peaks-only) spectrum.

The shape is deliberately broad and slowly varying -- exactly the kind of
background AsLS is designed to follow and subtract, and clearly distinguishable
from the sharp peaks a learner is trying to keep.
"""

from __future__ import annotations

import numpy as np

__all__ = ["fluorescence_background"]

# Where the broad fluorescence hump sits and how wide it is, both expressed as
# fractions of the axis span so the shape is independent of the real units
# (cm-1, nm, ...). Centre nearer the low end with a wide spread gives the
# characteristic "rise early, fall away slowly" fluorescence swell.
_CENTER_FRACTION = 0.35
_WIDTH_FRACTION = 0.35


def fluorescence_background(
    x: np.ndarray,
    magnitude: float,
    shape: str = "broad",
    seed: int | np.random.Generator | None = None,
) -> np.ndarray:
    """Build a broad, smooth fluorescence background over the axis ``x``.

    Returns a slowly varying curve whose maximum equals ``magnitude``, suitable
    for *adding* to a clean Raman spectrum to mimic the fluorescence swell that
    dwarfs the real peaks::

        raw = peaks + fluorescence_background(x, magnitude=3.0)

    The ``"broad"`` shape is a wide, smooth hump (a broad Gaussian placed about
    a third of the way along the axis), normalised so its peak is exactly
    ``magnitude``. It is intentionally broad and gently curved -- the kind of
    background AsLS baseline correction is built to follow and remove, and easy
    to tell apart from the sharp Lorentzian Raman lines on top of it.

    Parameters
    ----------
    x : numpy.ndarray
        The axis, shape ``(n_points,)`` (e.g. a Raman-shift axis in cm-1).
    magnitude : float
        Peak height of the background, in the units of the signal. ``0`` gives a
        flat zero background (fluorescence switched off). Must be non-negative.
        Choose it larger than the Raman peak amplitudes to reproduce the typical
        case where fluorescence dominates the raw spectrum.
    shape : str, optional
        Which background profile to build. Only ``"broad"`` (a wide smooth hump)
        is implemented; the parameter exists so the call signature stays stable
        if other background shapes are added later.
    seed : int or numpy.random.Generator or None, optional
        Reserved for a future stochastic background variation and **currently
        unused** -- the ``"broad"`` background is fully deterministic, so this
        argument has no effect for any value (including the default ``None``).
        It is kept in the signature only so the call stays stable when random
        variation is added later. Until then, the same ``x`` and ``magnitude``
        always give the same curve.

    Returns
    -------
    numpy.ndarray
        The background, same shape as ``x``. Non-negative, with maximum equal to
        ``magnitude``.

    Raises
    ------
    ValueError
        If ``magnitude`` is negative, or if ``shape`` is not ``"broad"``.

    Examples
    --------
    Deterministic, broad, and scaled so its peak is ``magnitude``:

    >>> import numpy as np
    >>> x = np.linspace(200, 3200, 1000)
    >>> bg = fluorescence_background(x, magnitude=3.0)
    >>> float(bg.max())
    3.0
    >>> bool((bg >= 0).all())
    True

    Switched off with ``magnitude=0``:

    >>> bool((fluorescence_background(x, magnitude=0.0) == 0).all())
    True
    """
    # `seed` is intentionally not used (see the parameter docs).
    if magnitude < 0:
        raise ValueError(f"magnitude must be non-negative; got {magnitude}.")
    if shape != "broad":
        raise ValueError(
            f"shape={shape!r} is not available; only 'broad' is implemented."
        )

    x = np.asarray(x, dtype=float)

    # Short-circuit the off case: no curve to build.
    if magnitude == 0:
        return np.zeros_like(x)

    # Map the axis onto 0..1 so the hump's position and width are independent of
    # the axis's real range. (x is strictly increasing, so span > 0.)
    span = x[-1] - x[0]
    t = (x - x[0]) / span

    # A broad Gaussian hump in normalised coordinates.
    bump = np.exp(-((t - _CENTER_FRACTION) ** 2) / (2.0 * _WIDTH_FRACTION**2))

    # Normalise so the maximum is exactly 1, then scale to `magnitude`. This
    # guarantees the peak height is `magnitude` regardless of where the hump's
    # crest lands relative to the sample grid.
    return magnitude * (bump / bump.max())
