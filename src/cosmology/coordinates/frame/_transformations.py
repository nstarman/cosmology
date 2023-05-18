"""The Cosmology coordinates library."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

__all__: list[str] = []

if TYPE_CHECKING:
    from collections.abc import Iterator

    from cosmology.coordinates.api.frame._base import CoordinateFrame
    from cosmology.coordinates.api.frame._core import Coordinate

FieldT = TypeVar("FieldT")


class CoordinateFrameTransformation(Protocol[FieldT]):
    """The Coordinate representation transform."""

    def __call__(
        self, from_coordinate: Coordinate[FieldT], to_frame: CoordinateFrame, /
    ) -> Coordinate[FieldT]:
        """Transform the Coordinate frame."""
        ...


class CoordinateFrameTransformationRegistry(Protocol[FieldT]):
    """The Coordinate representation transform registry."""

    def __getitem__(
        self, key: tuple[type[CoordinateFrame], type[CoordinateFrame]]
    ) -> CoordinateFrameTransformation[FieldT]:
        """Get the Coordinate representation transform."""
        ...

    def __contains__(
        self, key: tuple[type[CoordinateFrame], type[CoordinateFrame]]
    ) -> bool:
        """Check if the Coordinate representation transform is registered."""
        ...

    def __iter__(self) -> Iterator[tuple[type[CoordinateFrame], type[CoordinateFrame]]]:
        """Iterate over the Coordinate representation transform registry."""
        ...

    def __len__(self) -> int:
        """Get the number of Coordinate representation transforms registered."""
        ...
