"""Build the measurement axis shared by every technique.

A spectrum or chromatogram is intensities measured *against an axis*: nanometres
in UV-Vis, wavenumbers in Raman, m/z in mass spec, minutes in chromatography.
The physics differs but the axis is always the same idea -- a 1D array of evenly
spaced points -- so one builder serves them all.

:func:`build_axis` is that builder. You describe the axis one of two ways, and
it returns the points:

* by **count** -- "give me 400 points from 400 to 800 nm" (``n_points=400``);
* by **step** -- "give me a point every 2 cm-1 from 200 to 3500"
  (``step=2``).

Both endpoints are treated as inclusive of ``start``; see the parameter notes
for exactly how ``stop`` is handled in each mode.
"""

from __future__ import annotations

import numpy as np

__all__ = ["build_axis"]


def build_axis(
    start: float,
    stop: float,
    n_points: int | None = None,
    step: float | None = None,
) -> np.ndarray:
    """Build a 1D measurement axis.

    Specify the axis **either** by ``n_points`` (how many points) **or** by
    ``step`` (the spacing between points) -- exactly one of the two. Supplying
    both, or neither, is ambiguous and raises an error.

    Parameters
    ----------
    start : float
        First value of the axis (always included).
    stop : float
        Upper end of the axis. How it is treated depends on the mode:

        * with ``n_points`` -- ``stop`` is the exact last point (evenly spaced,
          endpoint included), like :func:`numpy.linspace`.
        * with ``step`` -- the axis advances from ``start`` in increments of
          ``step`` up to the largest value that does not exceed ``stop``. If
          ``stop - start`` is not a whole multiple of ``step``, the final point
          will be just below ``stop``.
    n_points : int, optional
        Number of points to generate. Must be at least 2. Mutually exclusive
        with ``step``.
    step : float, optional
        Spacing between consecutive points. Must be positive. Mutually exclusive
        with ``n_points``.

    Returns
    -------
    numpy.ndarray
        The axis, shape ``(n_points,)``, strictly increasing.

    Raises
    ------
    ValueError
        If neither or both of ``n_points``/``step`` are given; if
        ``stop <= start``; if ``n_points < 2``; or if ``step`` is not positive
        (or is larger than the whole span).

    Examples
    --------
    By count -- 5 evenly spaced points, endpoint included:

    >>> build_axis(400, 800, n_points=5)
    array([400., 500., 600., 700., 800.])

    By step -- a point every 2 units; ``stop`` is the ceiling, not necessarily
    a point:

    >>> build_axis(0, 9, step=2)
    array([0., 2., 4., 6., 8.])
    """
    # Exactly one of the two sizing arguments must be provided. Checking this
    # up front turns a subtle "which one wins?" question into a clear error.
    if (n_points is None) == (step is None):
        raise ValueError(
            "Specify exactly one of n_points or step (not both, not neither)."
        )

    if stop <= start:
        raise ValueError(f"stop ({stop}) must be greater than start ({start}).")

    # --- Mode 1: fixed number of points, endpoint included. ---
    if n_points is not None:
        if n_points < 2:
            raise ValueError(f"n_points must be at least 2; got {n_points}.")
        # linspace includes both endpoints, which is what people expect from
        # "N points from start to stop".
        return np.linspace(start, stop, n_points)

    # --- Mode 2: fixed step. ---
    # (step is not None here, guaranteed by the exclusivity check above.)
    if step <= 0:
        raise ValueError(f"step must be positive; got {step}.")

    span = stop - start
    if step > span:
        raise ValueError(
            f"step ({step}) is larger than the axis span ({span}); that would "
            "produce a single point. Use a smaller step or pass n_points."
        )

    # Number of intervals that fit within the span; +1 for the starting point.
    # The tiny epsilon guards against float round-off dropping a point when the
    # span is an exact multiple of step (e.g. 0..10 step 2 should reach 10).
    n = int(np.floor(span / step + 1e-9)) + 1

    # Build from integer indices times step so spacing is exactly `step` with no
    # accumulated floating-point drift. ``arange(..., dtype=float)`` keeps the
    # axis float even for integer start/step, so both modes return the same dtype.
    return start + step * np.arange(n, dtype=float)
