"""Instrument artifacts -- the pathologies real measurements suffer from.

Clean peaks on a smooth background is the ideal; real detectors add ugliness on
top. This module injects those pathologies *on purpose*, so a lesson has
something real to diagnose and clean.

The first one the Raman lessons need is the **cosmic ray**: a high-energy
particle hits the CCD during the exposure and dumps charge into one (or a few)
pixels, producing a razor-sharp, very tall spike that has *nothing* to do with
the chemistry. Cosmic rays are the classic "is that a peak or an artifact?"
trap -- they are narrow and tall where real Raman lines have a finite width, so
they can be found and removed (despiking) before any real analysis.

:func:`add_cosmic_rays` injects spikes and, crucially, **returns the indices it
spiked**, so a lesson can run a despiking algorithm and grade the hits/misses
against the known truth -- something real data can never offer. Saturation and
dropouts (the other classic artifacts) are deferred until a notebook needs them.
"""

from __future__ import annotations

import numpy as np

__all__ = ["add_cosmic_rays"]


def add_cosmic_rays(
    y: np.ndarray,
    n_spikes: int,
    intensity: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Add sharp cosmic-ray spikes to a single spectrum.

    Picks ``n_spikes`` distinct random positions and adds a tall, single-point
    positive spike at each. Spike heights vary a little (between ``intensity``
    and ``2 * intensity``) so they look like real cosmic-ray hits rather than a
    row of identical bars, but every spike is at least ``intensity`` tall -- set
    ``intensity`` well above the real peak heights to get the characteristic
    "obviously not chemistry" spikes.

    Unlike a plain in-place edit, this returns **both** the spiked spectrum and
    the array of indices it hit, mirroring the package convention (see
    :func:`simulated_data.core.scatter.apply_scatter`) of handing back the ground
    truth so a notebook can grade its despiking against the known spike
    locations.

    Parameters
    ----------
    y : numpy.ndarray
        A single spectrum, shape ``(n_points,)``. Not modified in place -- a
        copy is returned.
    n_spikes : int
        How many spikes to add. Must be between ``0`` and ``len(y)`` (you cannot
        place more distinct spikes than there are points). ``0`` returns an
        unchanged copy and draws **no** randomness, so disabling spikes leaves
        the generator's stream -- and any later draws -- untouched.
    intensity : float
        The minimum spike height added on top of ``y`` (each spike is between
        ``intensity`` and ``2 * intensity``). Must be non-negative.
    rng : numpy.random.Generator
        The generator to draw from. Pass the one your ``simulate*`` call already
        resolved from its ``seed`` so the result is reproducible. Never use
        NumPy's global ``np.random`` here -- that would break reproducibility.

    Returns
    -------
    y_spiked : numpy.ndarray
        A copy of ``y`` with the spikes added, same shape as ``y``.
    indices : numpy.ndarray
        The sorted indices that were spiked, shape ``(n_spikes,)`` (empty when
        ``n_spikes == 0``). This is the ground truth for grading despiking.

    Raises
    ------
    ValueError
        If ``y`` is not 1D, if ``n_spikes`` is negative or larger than
        ``len(y)``, or if ``intensity`` is negative.
    TypeError
        If ``rng`` is not a :class:`numpy.random.Generator`.

    Examples
    --------
    Two reproducible spikes, with their locations handed back for grading:

    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> y = np.zeros(100)
    >>> y_spiked, idx = add_cosmic_rays(y, n_spikes=2, intensity=5.0, rng=rng)
    >>> idx.shape
    (2,)
    >>> bool((y_spiked[idx] >= 5.0).all())     # every spike is at least `intensity`
    True

    Disabled with ``n_spikes=0`` -- unchanged, and no randomness drawn:

    >>> y_spiked, idx = add_cosmic_rays(y, n_spikes=0, intensity=5.0, rng=rng)
    >>> bool(np.array_equal(y_spiked, y)) and idx.size == 0
    True
    """
    y = np.asarray(y, dtype=float)
    if y.ndim != 1:
        raise ValueError(
            f"y must be 1D (a single spectrum); got {y.ndim}D with shape "
            f"{y.shape}."
        )
    if not isinstance(rng, np.random.Generator):
        raise TypeError(
            "rng must be a numpy.random.Generator (resolve it once in your "
            f"simulate call via resolve_rng); got {type(rng).__name__!r}."
        )

    n_points = y.shape[0]
    if n_spikes < 0:
        raise ValueError(f"n_spikes must be non-negative; got {n_spikes}.")
    if n_spikes > n_points:
        raise ValueError(
            f"n_spikes ({n_spikes}) cannot exceed the number of points "
            f"({n_points}); there aren't that many distinct positions to spike."
        )
    if intensity < 0:
        raise ValueError(f"intensity must be non-negative; got {intensity}.")

    y_spiked = y.copy()

    # Short-circuit the off case: no spikes, no randomness drawn (keeps the
    # generator stream identical whether or not spikes are enabled).
    if n_spikes == 0:
        return y_spiked, np.empty(0, dtype=int)

    # Distinct positions (no two cosmic rays land on the same pixel), and a
    # height in [intensity, 2*intensity] for each so the spikes look natural.
    indices = rng.choice(n_points, size=n_spikes, replace=False)
    heights = intensity * (1.0 + rng.random(n_spikes))
    y_spiked[indices] += heights

    # Return sorted indices so the ground truth reads left-to-right.
    return y_spiked, np.sort(indices)
