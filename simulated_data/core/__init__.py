"""Shared physics primitives for ``simulated_data``.

This is the building-block layer: axes, peak shapes, baselines, and noise. The
technique modules (``uvvis``, and later ``nir``/``raman``/...) *compose* these
primitives -- the physics lives here once, so a fix here fixes every technique.

Most lessons import a technique module from the top level
(``from simulated_data import uvvis``) and never touch ``core`` directly. Only a
notebook that is specifically *about* the physics -- e.g. "what is a Gaussian
peak?" -- imports these functions, which is why they are re-exported here for
convenience::

    from simulated_data.core import gaussian, build_axis

Phase 1 implemented the minimal set the early UV-Vis lessons need; ``scatter``
(the per-sample multiplicative/additive distortion behind SNV/MSC) was added for
the NIR lessons. The Raman lessons add the **Lorentzian** peak shape, the broad
**fluorescence** background, and **cosmic-ray** artifacts. Voigt peaks,
shot/pink noise, saturation, and dropouts are still deferred.
"""

from __future__ import annotations

from .artifacts import add_cosmic_rays
from .axes import build_axis
from .background import fluorescence_background
from .baselines import curved_baseline, sloping_baseline
from .noise import gaussian_noise
from .peaks import add_peaks, gaussian, lorentzian
from .scatter import apply_scatter

__all__ = [
    "build_axis",
    "gaussian",
    "lorentzian",
    "add_peaks",
    "sloping_baseline",
    "curved_baseline",
    "gaussian_noise",
    "apply_scatter",
    "fluorescence_background",
    "add_cosmic_rays",
]
