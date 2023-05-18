"""The Cosmology coordinates library."""


from dataclasses import dataclass

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.representation._base._base import CoordinateRepresentation


@dataclass(frozen=True)
class Cartesian(CoordinateRepresentation[ArrayT]):
    """One-dimensional coordinate.

    Parameters
    ----------
    x : ArrayT
        Coordinate.
    """

    x: ArrayT
