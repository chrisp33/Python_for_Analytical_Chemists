"""Baselines -- the slow, broad trend a real spectrum sits on top of.

No instrument gives you peaks on a perfectly flat zero. There is always a
background: a sloping drift from a dirty cuvette or lamp ageing, or a gentle
curve from scattering and optics. Removing that background (baseline correction)
is a core skill -- but to *teach* removing it, you first need data that *has* a
realistic baseline to remove. That's what this module makes.

Phase 1 provides two shapes, the two the early UV-Vis lessons need:

* :func:`sloping_baseline` -- a straight tilt (offset + slope).
* :func:`curved_baseline` -- a smooth bow, the kind asymmetric-least-squares
  (AsLS) baseline correction is designed to handle.

Both return an array the same length as the axis, meant to be *added* to a clean
spectrum.
"""

from __future__ import annotations

import numpy as np

__all__ = ["sloping_baseline", "curved_baseline"]


def sloping_baseline(x: np.ndarray, slope: float, offset: float) -> np.ndarray:
    """Build a straight-line (linear) baseline.

    The simplest realistic background: a constant tilt across the axis, as if
    the whole spectrum sits on a ramp. Measured from the *start* of the axis, so
    the parameters read intuitively:

    * ``offset`` is the baseline value at the first axis point;
    * ``slope`` is how much it rises (or falls) per unit of ``x``.

    Anchoring at ``x[0]`` means ``offset`` stays meaningful no matter where the
    axis starts -- a UV-Vis axis beginning at 400 nm behaves the same as one
    beginning at 0.

    Parameters
    ----------
    x : numpy.ndarray
        The axis, shape ``(n_points,)``.
    slope : float
        Rise in baseline per unit of ``x``. Positive tilts upward toward higher
        ``x``; negative tilts downward; ``0`` gives a flat offset.
    offset : float
        Baseline value at the first axis point, ``x[0]``.

    Returns
    -------
    numpy.ndarray
        The baseline, same shape as ``x``.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([400.0, 401.0, 402.0])
    >>> sloping_baseline(x, slope=0.01, offset=0.1)
    array([0.1 , 0.11, 0.12])
    """
    x = np.asarray(x, dtype=float)
    return offset + slope * (x - x[0])


def curved_baseline(
    x: np.ndarray,
    magnitude: float,
    curvature: float,
    seed: int | np.random.Generator | None = None,
) -> np.ndarray:
    """Build a smooth, curved baseline (a gentle bow across the axis).

    A more realistic background than a straight line: it starts at zero and
    rises to ``magnitude`` at the far end of the axis, bending on the way. The
    bend is set by ``curvature``, which morphs the shape from a straight ramp
    into a quadratic curve::

        t = (x - x.min()) / (x.max() - x.min())          # axis mapped to 0..1
        baseline = magnitude * ((1 - curvature) * t + curvature * t**2)

    so ``curvature=0`` is a straight ramp and ``curvature=1`` is a fully
    quadratic bow (slow start, steep finish). Either way the baseline equals
    ``0`` at the start and ``magnitude`` at the end.

    This smooth, slowly varying shape is exactly the kind of background that
    asymmetric-least-squares (AsLS) correction is built to subtract, which makes
    it the right baseline for the AsLS lesson.

    Parameters
    ----------
    x : numpy.ndarray
        The axis, shape ``(n_points,)``.
    magnitude : float
        Baseline height at the far end of the axis (its overall size).
    curvature : float
        How curved the baseline is. ``0`` -> straight ramp; ``1`` -> quadratic
        bow. Values in between blend the two; values outside ``[0, 1]`` are
        allowed for stronger or inverted bends.
    seed : int or numpy.random.Generator or None, optional
        Reserved for a future stochastic baseline variation and **currently
        unused** -- in Phase 1 the curved baseline is fully deterministic, so
        this argument has no effect for any value (including the default
        ``None``). It is kept in the signature only so the call stays stable
        when random variation is added in a later phase, behind an explicit
        opt-in. Until then, the same ``magnitude``/``curvature`` always give the
        same curve.

    Returns
    -------
    numpy.ndarray
        The baseline, same shape as ``x``.

    Examples
    --------
    Deterministic; zero at the start, ``magnitude`` at the end:

    >>> import numpy as np
    >>> x = np.linspace(0, 1, 5)
    >>> b = curved_baseline(x, magnitude=2.0, curvature=1.0)
    >>> float(b[0]), float(b[-1])
    (0.0, 2.0)
    """
    # `seed` is intentionally not used in Phase 1 (see the parameter docs).
    x = np.asarray(x, dtype=float)

    # Map the axis onto 0..1 so the shape is independent of the axis's real
    # range. (x is strictly increasing, so span > 0 for any valid axis.)
    span = x[-1] - x[0]
    t = (x - x[0]) / span

    # Blend a straight ramp (t) with a quadratic (t**2); both hit `magnitude`
    # at t = 1, so `magnitude` is always the height at the far end.
    return magnitude * ((1.0 - curvature) * t + curvature * t**2)
