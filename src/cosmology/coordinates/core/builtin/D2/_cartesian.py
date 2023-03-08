"""The Cosmology coordinates library."""

from __future__ import annotations

from dataclasses import dataclass

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.core.builtin.d1 import Cartesian as Cartesian1D

__all__: list[str] = []


@dataclass(frozen=True, eq=False)
class Cartesian(Cartesian1D[ArrayT]):
    """Two-dimensional Cartesian coordinates.

    Parameters
    ----------
    x, y : Array
        Coordinate.
    """

    y: ArrayT
