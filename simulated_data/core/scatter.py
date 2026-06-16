"""Physical scatter -- the sample-to-sample distortion that *defines* NIR.

In diffuse-reflectance techniques (NIR above all), light doesn't just get
absorbed by the chemistry; it bounces around the sample first. Particle size,
packing density, and surface texture all change how much light comes back,
**independently of the chemical composition**. The result is that two samples
with identical chemistry can produce wildly different-looking spectra -- one
shifted up, one tilted -- so the real information is buried under a physical
artefact.

The standard, and remarkably good, model for that artefact is *affine* and
*per-sample*: every spectrum is multiplied by its own slope and shifted by its
own offset::

    x_measured[i] = slope[i] * x_true[i] + offset[i]

The multiplicative ``slope`` captures path-length / scattering-efficiency
differences; the additive ``offset`` captures a baseline shift. This is exactly
the model that Standard Normal Variate (SNV) and Multiplicative Scatter
Correction (MSC) are built to undo -- which is why teaching NIR preprocessing
*requires* data that has this distortion in it on purpose.

:func:`apply_scatter` injects that distortion. Crucially it also **returns the
true per-sample slope and offset it used**, so a lesson can apply SNV/MSC and
grade the recovered chemistry against the known truth -- something real data can
never offer.
"""

from __future__ import annotations

import numpy as np

__all__ = ["apply_scatter"]


def apply_scatter(
    X: np.ndarray,
    slope_sigma: float,
    offset_sigma: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Apply per-sample multiplicative + additive scatter to a data matrix.

    Each row (one spectrum) gets its *own* random slope and offset::

        slope[i]  = 1 + N(0, slope_sigma)      # multiplicative, centred on 1
        offset[i] =     N(0, offset_sigma)      # additive,       centred on 0
        X_scattered[i] = slope[i] * X[i] + offset[i]

    The slope is centred on ``1`` (no scaling) and the offset on ``0`` (no
    shift), so ``slope_sigma`` and ``offset_sigma`` are the *strengths* of the
    two effects -- larger sigma, more spaghetti. With both at ``0`` the data is
    returned unchanged and no randomness is drawn.

    The function returns the true ``slope`` and ``offset`` arrays alongside the
    distorted data, so the caller can record them as ground truth (this is what
    lets a notebook grade SNV/MSC against the real scatter).

    Parameters
    ----------
    X : numpy.ndarray
        The clean data matrix, shape ``(n_samples, n_points)`` -- one spectrum
        per row. Always 2D, matching the package's :class:`~simulated_data.Dataset`
        convention.
    slope_sigma : float
        Standard deviation of the per-sample multiplicative factor about ``1``.
        Must be non-negative. Controls how much the spectra fan out in scale.
    offset_sigma : float
        Standard deviation of the per-sample additive offset about ``0``. Must
        be non-negative. Controls how much the spectra shift up and down.
    rng : numpy.random.Generator
        The generator to draw from. Pass the one your ``simulate*`` call already
        resolved from its ``seed`` so the result is reproducible. Never use
        NumPy's global ``np.random`` here -- that would break reproducibility.

    Returns
    -------
    X_scattered : numpy.ndarray
        The distorted data, same shape as ``X``.
    slope : numpy.ndarray
        The true per-sample multiplicative factor, shape ``(n_samples,)``.
    offset : numpy.ndarray
        The true per-sample additive offset, shape ``(n_samples,)``.

    Raises
    ------
    ValueError
        If ``X`` is not 2D, or if either sigma is negative.
    TypeError
        If ``rng`` is not a :class:`numpy.random.Generator`.

    Examples
    --------
    Per-sample distortion, with the truth handed back for grading:

    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> X = np.ones((3, 5))
    >>> Xs, slope, offset = apply_scatter(X, 0.05, 0.1, rng)
    >>> Xs.shape
    (3, 5)
    >>> slope.shape, offset.shape
    ((3,), (3,))

    With both strengths at zero the data passes through untouched:

    >>> Xs, slope, offset = apply_scatter(X, 0.0, 0.0, rng)
    >>> bool(np.array_equal(Xs, X))
    True
    >>> bool((slope == 1).all()) and bool((offset == 0).all())
    True
    """
    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError(
            "X must be 2D with shape (n_samples, n_points); got "
            f"{X.ndim}D with shape {X.shape}."
        )
    if slope_sigma < 0:
        raise ValueError(f"slope_sigma must be non-negative; got {slope_sigma}.")
    if offset_sigma < 0:
        raise ValueError(f"offset_sigma must be non-negative; got {offset_sigma}.")
    if not isinstance(rng, np.random.Generator):
        raise TypeError(
            "rng must be a numpy.random.Generator (resolve it once in your "
            f"simulate call via resolve_rng); got {type(rng).__name__!r}."
        )

    n_samples = X.shape[0]

    # Draw the per-sample distortion. Each sigma is short-circuited at 0 so a
    # disabled effect draws no randomness (keeping the generator stream -- and
    # therefore later noise -- identical whether or not that effect is on).
    if slope_sigma > 0:
        slope = 1.0 + rng.normal(0.0, slope_sigma, size=n_samples)
    else:
        slope = np.ones(n_samples)

    if offset_sigma > 0:
        offset = rng.normal(0.0, offset_sigma, size=n_samples)
    else:
        offset = np.zeros(n_samples)

    # Affine, per-sample: (n_samples, 1) * (n_samples, n_points) + (n_samples, 1).
    X_scattered = slope[:, np.newaxis] * X + offset[:, np.newaxis]
    return X_scattered, slope, offset
