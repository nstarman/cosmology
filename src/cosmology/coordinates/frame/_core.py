"""The cosmological coordinates API standard."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from cosmology.coordinates.api._array_api import ArrayT
from cosmology.coordinates.api._array_mixin import ArrayCoordinateMixin
from cosmology.coordinates.api.representation._base import (
    CoordinateRepresentation,
    FieldT,
)

__all__: list[str] = []

if TYPE_CHECKING:
    from cosmology.coordinates.api.frame._base import CoordinateFrame
    from cosmology.coordinates.api.representation._space import (
        CoordinateRepresentationPhaseSpace,
    )

CrdT = TypeVar("CrdT", bound="CoordinateRepresentation[FieldT]")  # type: ignore[valid-type]  # noqa: E501


class Coordinate(CoordinateRepresentation[FieldT]):
    """The API for Coordinate Frames.

    Parameters
    ----------
    data : CoordinateRepresentationPhaseSpace[FieldT]
        The data for the coordinate.
    frame : CoordinateFrame
        The coordinate frame of the data.
    """

    data: CoordinateRepresentationPhaseSpace[FieldT]
    frame: CoordinateFrame

    def to_coordinate_frame(self: CrdT, frame: type[CoordinateFrame], /) -> CrdT:
        """Transform the coordinate to the given frame.

        Parameters
        ----------
        frame : type[CoordinateFrame]
            The frame to transform to.

        Returns
        -------
        Coordinate[FieldT]
            The transformed coordinate.
        """
        ...


class ArrayCoordinate(ArrayCoordinateMixin[ArrayT], Coordinate[ArrayT]):
    ...
