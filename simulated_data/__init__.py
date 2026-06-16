"""``simulated_data`` -- realistic, reproducible synthetic data for lessons.

This package generates scientifically honest stand-in data (UV-Vis, NIR, and
Raman spectra so far; more techniques later) so every notebook in the *Python
for Analytical Chemists* series runs offline, reproducibly, and without data-
licensing headaches. Because the data is simulated, each dataset also carries
its own ground truth in ``meta`` -- so a lesson can grade its analysis against
the real answer.

How to use it in a lesson -- import the **module**, then call its ``simulate``
function (this reads clearly and keeps the technique obvious)::

    from simulated_data import uvvis

    ds = uvvis.simulate(seed=0)   # a reproducible UV-Vis spectrum
    ds.x        # the wavelength axis
    ds.X        # the data, always 2D: (n_samples, n_points)
    ds.meta     # one row per sample, with the TRUE parameters used

The shared return type is :class:`Dataset`; import it directly when you need to
reference it (e.g. for type hints)::

    from simulated_data import Dataset

Reproducibility contract: every generator takes ``seed`` and never touches
NumPy's global random state, so ``simulate(seed=0)`` gives identical data on any
machine. Lessons should always set a seed so viewers reproduce the figures.
"""

from __future__ import annotations

from . import nir, raman, uvvis
from .types import Dataset

__version__ = "0.1.0"

# Only the technique modules and the shared return type are part of the public
# surface. The `core` physics layer and the internal `_rng` helper are reachable
# (`simulated_data.core`, etc.) but intentionally left out of `__all__`: lessons
# import from the top level, not from internals.
__all__ = ["uvvis", "nir", "raman", "Dataset", "__version__"]
