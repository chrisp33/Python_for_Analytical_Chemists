"""The one return type every generator shares: :class:`Dataset`.

Every ``simulate*`` function in this package returns a ``Dataset``. That single
promise is what makes the lessons feel consistent -- once a learner knows how to
unpack one technique's output, they know them all.

The mental model is the way spectra actually live on disk and in instruments:

* one shared **axis** (``x``) -- wavelengths, wavenumbers, m/z, or time;
* a **data matrix** (``X``) of intensities, *always* 2D as ``(n_samples,
  n_points)`` -- even a single spectrum is stored as one row, so there is never
  a "is this 1D or 2D?" special case to reason about;
* optional **reference values** (``y``) -- e.g. the concentration behind each
  spectrum, or ``None`` when there is no target;
* a **metadata table** (``meta``) -- one row per sample carrying the *true*
  parameters used to build it, so a notebook can grade its analysis against the
  real answer (something real data can never offer);
* **labels and units** that travel with the data so plots come out correct
  automatically.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

__all__ = ["Dataset"]


@dataclass
class Dataset:
    """A simulated dataset: a shared axis plus one or more intensity vectors.

    This is the universal return type of the package. See the module docstring
    for the mental model. The two beginner conveniences are :meth:`single`
    (grab the lone spectrum when there's only one) and :meth:`to_frame` (get a
    tidy, wide :class:`pandas.DataFrame` for inspection or export).

    Attributes
    ----------
    x : numpy.ndarray
        The shared axis, shape ``(n_points,)``. One axis for every sample.
    X : numpy.ndarray
        The data matrix, shape ``(n_samples, n_points)`` -- **always 2D**, even
        for a single spectrum (which is stored as ``(1, n_points)``).
    y : numpy.ndarray or None
        Reference/target values, shape ``(n_samples,)``, or ``None`` when the
        dataset has no associated target (e.g. a one-off spectrum).
    meta : pandas.DataFrame
        One row per sample. Holds ids, the ground-truth parameters used to
        generate each sample, and any labels. Must have exactly ``n_samples``
        rows.
    x_label : str
        Human-readable name of the axis, e.g. ``"Wavelength"``.
    x_unit : str
        Unit of the axis, e.g. ``"nm"`` or ``"cm-1"``.
    y_label : str
        Name of the measured quantity, e.g. ``"Absorbance"`` or ``"Intensity"``.

    Notes
    -----
    On construction the dataclass validates the shape contract that every
    downstream notebook relies on: ``x`` is 1D, ``X`` is 2D, ``X`` has one
    column per axis point, ``y`` (if present) has one value per sample, and
    ``meta`` has one row per sample. ``x``, ``X``, and ``y`` are coerced to
    NumPy arrays so the object is robust even if built by hand in a lesson.
    """

    x: np.ndarray
    X: np.ndarray
    y: np.ndarray | None
    meta: pd.DataFrame
    x_label: str
    x_unit: str
    y_label: str

    def __post_init__(self) -> None:
        """Coerce array fields and enforce the shape contract.

        Runs automatically right after the dataclass is built. Catching a
        malformed dataset *here* -- at creation -- gives a clear error at the
        source, instead of a confusing failure deep inside a later notebook.
        """
        # Coerce the numeric fields to float arrays. This makes the Dataset
        # forgiving of hand-built inputs (lists, tuples) while guaranteeing the
        # rest of the package always sees real ndarrays.
        self.x = np.asarray(self.x, dtype=float)
        self.X = np.asarray(self.X, dtype=float)
        if self.y is not None:
            self.y = np.asarray(self.y)

        # --- Shape contract: the invariants every notebook depends on. ---
        if self.x.ndim != 1:
            raise ValueError(
                f"x must be 1D (the shared axis); got {self.x.ndim}D "
                f"with shape {self.x.shape}."
            )
        if self.X.ndim != 2:
            raise ValueError(
                "X must always be 2D with shape (n_samples, n_points); got "
                f"{self.X.ndim}D with shape {self.X.shape}. A single spectrum "
                "should be stored as shape (1, n_points)."
            )

        n_samples, n_points = self.X.shape

        if n_points != self.x.shape[0]:
            raise ValueError(
                "X has one column per axis point, so X.shape[1] must equal "
                f"len(x); got X.shape[1]={n_points} and len(x)={self.x.shape[0]}."
            )
        if self.y is not None and self.y.shape[0] != n_samples:
            raise ValueError(
                "y holds one reference value per sample, so len(y) must equal "
                f"n_samples; got len(y)={self.y.shape[0]} and "
                f"n_samples={n_samples}."
            )
        if len(self.meta) != n_samples:
            raise ValueError(
                "meta holds one row per sample, so it must have n_samples rows; "
                f"got {len(self.meta)} rows and n_samples={n_samples}."
            )

    def single(self) -> np.ndarray:
        """Return the lone spectrum as a 1D array.

        A beginner shortcut for the common case of a one-sample dataset: rather
        than remembering to write ``ds.X[0]``, call ``ds.single()``. It refuses
        to guess when there is more than one sample, so you never silently get
        "just the first one".

        Returns
        -------
        numpy.ndarray
            The single intensity vector, shape ``(n_points,)``.

        Raises
        ------
        ValueError
            If the dataset contains more than one sample.

        Examples
        --------
        >>> from simulated_data import uvvis
        >>> ds = uvvis.simulate(seed=0)
        >>> ds.single().shape == (ds.x.shape[0],)
        True
        """
        n_samples = self.X.shape[0]
        if n_samples != 1:
            raise ValueError(
                f"single() is only valid when there is one sample, but this "
                f"dataset has {n_samples}. Index X directly, e.g. ds.X[i]."
            )
        return self.X[0]

    def to_frame(self) -> pd.DataFrame:
        """Return a wide :class:`pandas.DataFrame`: samples x axis points.

        Handy for a quick look, for ``.head()`` in a notebook, or for exporting
        to CSV. The layout is one row per sample, with the metadata columns
        first (so the ground truth is right there next to the data), followed by
        one column per axis point -- each column labelled with its axis value
        (e.g. the wavelength).

        Returns
        -------
        pandas.DataFrame
            Shape ``(n_samples, n_meta_columns + n_points)``. The index matches
            ``meta``'s index so sample ids carry through.

        Examples
        --------
        >>> from simulated_data import uvvis
        >>> ds = uvvis.simulate(n_samples=3, seed=0)
        >>> frame = ds.to_frame()
        >>> frame.shape[0]
        3
        """
        # Spectral block: rows = samples, columns = the axis values themselves.
        # Reusing meta's index keeps sample identity consistent across both
        # blocks when we concatenate.
        spectra = pd.DataFrame(self.X, columns=self.x, index=self.meta.index)

        # Meta first, then spectra -- truth columns sit on the left, easy to
        # read before the wall of intensity columns.
        return pd.concat([self.meta, spectra], axis=1)
