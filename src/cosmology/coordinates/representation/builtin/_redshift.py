"""The Cosmology coordinates library."""

from dataclasses import dataclass

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.representation._base._base import CoordinateRepresentation


@dataclass(frozen=True)
class RedshiftRepresentation(CoordinateRepresentation[ArrayT]):
    """Redshift cosmology representation.

    Parameters
    ----------
    redshift : ArrayT
        Redshift.
    """

    redshift: ArrayT


@dataclass(frozen=True)
class RedshiftAndDistance(RedshiftRepresentation[ArrayT]):
    """Redshift and distance cosmology representation.

    Parameters
    ----------
    redshift : ArrayT
        Redshift.
    distance : ArrayT
        Distance.
    """

    distance: ArrayT


@dataclass(frozen=True)
class RedshiftAndTime(RedshiftRepresentation[ArrayT]):
    """Redshift and time cosmology representation.

    Parameters
    ----------
    redshift : ArrayT
        Redshift.
    time : ArrayT
        Time.
    """

    time: ArrayT
