"""Measurement noise -- the random scatter on every real reading.

No detector returns the exact same number twice. Phase 1 models the most common
and most teachable kind: **Gaussian (normal) noise** with a constant spread, the
"random jitter" that smoothing (e.g. Savitzky-Golay) is meant to reduce. Signal-
dependent shot noise and 1/f pink noise are deferred to later phases.

This module deliberately takes an already-resolved
:class:`numpy.random.Generator` rather than a ``seed``. The pattern across the
package is: a ``simulate*`` function resolves the seed **once** (via
:func:`simulated_data._rng.resolve_rng`) and threads that one generator through
every random step -- noise included -- so the whole spectrum is reproducible
from a single seed.
"""

from __future__ import annotations

import numpy as np

__all__ = ["gaussian_noise"]


def gaussian_noise(
    shape: int | tuple[int, ...],
    level: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Draw Gaussian (normal) noise with constant standard deviation.

    Returns an array of independent normal samples with mean ``0`` and standard
    deviation ``level``. Add it to a clean signal to simulate detector noise::

        noisy = clean + gaussian_noise(clean.shape, level=0.005, rng=rng)

    Parameters
    ----------
    shape : int or tuple of int
        Shape of the noise array, e.g. ``n_points`` for one spectrum or
        ``(n_samples, n_points)`` for a whole batch. Matching the signal's shape
        makes the noise independent at every point and every sample.
    level : float
        Standard deviation (sigma) of the noise -- its typical size in the units
        of the signal. Must be non-negative. ``0`` returns all zeros (a clean,
        noise-free signal).
    rng : numpy.random.Generator
        The generator to draw from. Pass the one your ``simulate*`` call already
        resolved from its ``seed`` so the result is reproducible. Never use
        NumPy's global ``np.random`` here -- that would break reproducibility.

    Returns
    -------
    numpy.ndarray
        Noise array of the requested ``shape``.

    Raises
    ------
    ValueError
        If ``level`` is negative.
    TypeError
        If ``rng`` is not a :class:`numpy.random.Generator`.

    Examples
    --------
    Reproducible from a shared generator; ``level=0`` gives no noise:

    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> n = gaussian_noise(5, level=0.1, rng=rng)
    >>> n.shape
    (5,)
    >>> bool((gaussian_noise(5, level=0.0, rng=rng) == 0).all())
    True
    """
    if level < 0:
        raise ValueError(f"level (noise sigma) must be non-negative; got {level}.")
    if not isinstance(rng, np.random.Generator):
        raise TypeError(
            "rng must be a numpy.random.Generator (resolve it once in your "
            "simulate call via resolve_rng); got "
            f"{type(rng).__name__!r}."
        )

    # Short-circuit the zero case: no randomness drawn, so a level=0 call never
    # disturbs the generator's stream for later steps.
    if level == 0:
        return np.zeros(shape)

    return rng.normal(loc=0.0, scale=level, size=shape)
