"""The Cosmology coordinates library."""


from dataclasses import dataclass

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.core._core import BaseCoordinate


@dataclass(frozen=True)
class Cartesian(BaseCoordinate[ArrayT]):
    """One-dimensional coordinate.

    Parameters
    ----------
    x : ArrayT
        Coordinate.
    """

    x: ArrayT
