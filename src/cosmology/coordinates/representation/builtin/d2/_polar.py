"""The Cosmology coordinates library."""

from __future__ import annotations

from dataclasses import dataclass

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.representation._base._base import CoordinateRepresentation

__all__: list[str] = []


@dataclass(frozen=True, eq=False)
class Polar(CoordinateRepresentation[ArrayT]):
    """Two-dimensional Cartesian coordinates.

    Parameters
    ----------
    rho, phi : Array
        Coordinate.
    """

    rho: ArrayT
    phi: ArrayT


@dataclass(frozen=True, eq=False)
class LogPolar(CoordinateRepresentation[ArrayT]):
    """Two-dimensional Cartesian coordinates.

    Parameters
    ----------
    rho, phi : Array
        Coordinate.
    """

    rho: ArrayT
    phi: ArrayT
