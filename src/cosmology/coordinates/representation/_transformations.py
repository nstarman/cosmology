"""The Cosmology coordinates library."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, cast

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.api.representation._transformations import (
    CoordinateRepresentationTransformationRegistry as CoordinateRepresentationTransformationRegistryAPI,  # noqa: E501
)

__all__: list[str] = []

if TYPE_CHECKING:
    from collections.abc import Iterator

    from cosmology.coordinates.representation._base._base import (
        CoordinateRepresentation,
        CrdT,
    )


###############################################################################
# PARAMETERS


class CoordinateRepresentationTransformationRegistry(
    CoordinateRepresentationTransformationRegistryAPI[ArrayT]
):
    """The CoordinateRepresentation transformation registry."""

    def __init__(self) -> None:
        """Initialize."""
        self._dict: dict[
            tuple[
                type[CoordinateRepresentation[ArrayT]],
                type[CoordinateRepresentation[ArrayT]],
            ],
            Callable[
                [CoordinateRepresentation[ArrayT]], CoordinateRepresentation[ArrayT]
            ],
        ] = {}

    def __getitem__(
        self,
        key: tuple[
            type[CoordinateRepresentation[ArrayT]],
            type[CoordinateRepresentation[ArrayT]],
        ],
    ) -> Callable[[CoordinateRepresentation[ArrayT]], CoordinateRepresentation[ArrayT]]:
        """Get the CoordinateRepresentation transformation."""
        return self._dict[key]

    def __contains__(
        self,
        key: tuple[
            type[CoordinateRepresentation[ArrayT]],
            type[CoordinateRepresentation[ArrayT]],
        ],
    ) -> bool:
        """Check if the CoordinateRepresentation transformation is registered."""
        return key in self._dict

    def __iter__(
        self,
    ) -> Iterator[
        tuple[
            type[CoordinateRepresentation[ArrayT]],
            type[CoordinateRepresentation[ArrayT]],
        ]
    ]:
        """Iterate over the CoordinateRepresentation transformation registry."""
        return iter(self._dict)

    def __len__(self) -> int:
        """Get the number of CoordinateRepresentation transformations."""
        return len(self._dict)


_GLBAL_COORDINATE_REPRESENTATION_TRANSFORMS = (
    CoordinateRepresentationTransformationRegistry()
)


###############################################################################
# EXCEPTIONS


class CoordinateRepresentationTransformError(Exception):
    """The CoordinateRepresentation transform error."""


class CoordinateRepresentationTransformNotImplementedError(
    CoordinateRepresentationTransformError,
):
    """The CoordinateRepresentation transform not implemented error."""


###############################################################################
# FUNCTIONS


def to_coordinate_representation(
    from_coordinate: CoordinateRepresentation[ArrayT],
    representation_type: type[CrdT],
    /,
    *coordinates: CoordinateRepresentation[ArrayT],
    representation_registry: CoordinateRepresentationTransformationRegistry[ArrayT]
    | None = None,
) -> CrdT:
    """Return the coordinate in a new representation.

    Parameters
    ----------
    from_coordinate : CoordinateRepresentation[ArrayT]
        The CoordinateRepresentation to transform.
    representation_type : type, positional-only
        Coordinate class to transform to.

    *coordinates : Coordinate, optional
        Additional coordinates required to transform to the new
        representation, e.g. differentials require a position coordinate.

    representation_registry : CoordinateRepresentationTransformationRegistry, optional
        Registry of representation transformations.
        If `None` (default), use the default global registry.

    Returns
    -------
    CoordinateRepresentation[ArrayT]
        The cosmology represented as a CoordinateRepresentation.
    """
    key = (type(from_coordinate), representation_type)
    if key not in _GLBAL_COORDINATE_REPRESENTATION_TRANSFORMS:
        msg = f"there is no registered transform from {key[0].__name__} to {key[1].__name__}"  # noqa: E501
        raise CoordinateRepresentationTransformNotImplementedError(msg)

    return cast(
        "CrdT",
        _GLBAL_COORDINATE_REPRESENTATION_TRANSFORMS[key](
            from_coordinate,
        ),
    )


def register_representation_transform(
    from_coordinate_type: type[CoordinateRepresentation[ArrayT]],
    to_coordinate: type[CoordinateRepresentation[ArrayT]],
) -> Callable[
    [Callable[[CoordinateRepresentation[ArrayT]], CoordinateRepresentation[ArrayT]]],
    Callable[[CoordinateRepresentation[ArrayT]], CoordinateRepresentation[ArrayT]],
]:
    """Register a CoordinateRepresentation transform.

    Parameters
    ----------
    from_coordinate_type : type[CoordinateRepresentation[ArrayT]]
        The CoordinateRepresentation class to transform from.
    to_coordinate : type[CoordinateRepresentation[ArrayT]]
        The CoordinateRepresentation class to transform to.

    Returns
    -------
    Callable
        The decorator.
    """

    def decorator(
        func: Callable[
            [CoordinateRepresentation[ArrayT]], CoordinateRepresentation[ArrayT]
        ],
    ) -> Callable[[CoordinateRepresentation[ArrayT]], CoordinateRepresentation[ArrayT]]:
        """Registration decorator."""
        _GLBAL_COORDINATE_REPRESENTATION_TRANSFORMS[
            from_coordinate_type,
            to_coordinate,
        ] = func
        return func

    return decorator
