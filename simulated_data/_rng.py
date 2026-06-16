"""Random-number generation for ``simulated_data`` (internal module).

Reproducibility is a contract in this package: the *same* seed must always
produce the *same* data, on any machine, every run. To make that possible,
every generator funnels its randomness through a single
:class:`numpy.random.Generator` and **never** touches NumPy's global random
state (``np.random.seed`` / ``np.random.rand`` / ...).

This module exposes exactly one helper, :func:`resolve_rng`, which turns the
flexible ``seed`` argument that learners pass at the top level
(``None`` / ``int`` / an existing ``Generator``) into a concrete
``Generator`` that the rest of the package can thread through unchanged.

The leading underscore in the filename signals "internal": lessons import
``uvvis``/``Dataset`` from the top level, not from here.
"""

from __future__ import annotations

import numpy as np

# Public name of this small module. Keeping ``__all__`` explicit documents the
# one symbol we intend other modules to use.
__all__ = ["resolve_rng"]


def resolve_rng(seed: int | np.random.Generator | None = None) -> np.random.Generator:
    """Turn a ``seed`` argument into a NumPy random ``Generator``.

    This is the single place the whole package decides "where does randomness
    come from?". Every ``simulate*`` function calls it once and passes the
    returned generator down into the core primitives, so randomness is both
    reproducible and fully local (the global ``np.random`` state is left
    untouched).

    Parameters
    ----------
    seed : int or numpy.random.Generator or None, optional
        Controls reproducibility:

        * ``int`` -- create a fresh generator seeded with this value. The same
          integer always yields the same data. **Use this in lessons** so
          viewers reproduce your exact figures.
        * ``numpy.random.Generator`` -- use it as-is. This lets advanced users
          share one generator across several calls (e.g. to build a larger
          experiment) while keeping the whole thing reproducible from one seed.
        * ``None`` (default) -- create a fresh, unpredictable generator. Each
          call returns different data. Good for "just show me something"
          exploration, bad for reproducible figures.

    Returns
    -------
    numpy.random.Generator
        A generator ready to draw random numbers from.

    Raises
    ------
    TypeError
        If ``seed`` is not an ``int``, a ``Generator``, or ``None``.

    Examples
    --------
    >>> rng_a = resolve_rng(0)
    >>> rng_b = resolve_rng(0)
    >>> bool((rng_a.standard_normal(3) == rng_b.standard_normal(3)).all())
    True

    Passing an existing generator returns that same object unchanged:

    >>> g = np.random.default_rng(42)
    >>> resolve_rng(g) is g
    True
    """
    # Already a Generator: hand it straight back so callers can share one
    # stream of randomness across multiple draws.
    if isinstance(seed, np.random.Generator):
        return seed

    # None or an int are both accepted directly by ``default_rng``:
    #   default_rng(None) -> fresh, OS-entropy-seeded generator
    #   default_rng(5)    -> deterministic generator seeded with 5
    # Note: ``bool`` is a subclass of ``int`` in Python, so we reject it
    # explicitly -- ``seed=True`` is almost certainly a mistake, not "seed 1".
    if seed is None or (isinstance(seed, int) and not isinstance(seed, bool)):
        return np.random.default_rng(seed)

    raise TypeError(
        "seed must be an int, a numpy.random.Generator, or None; "
        f"got {type(seed).__name__!r}."
    )
