"""The Cosmology coordinates library."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, cast

if TYPE_CHECKING:
    from cosmology.api._array_api import ArrayT
    from cosmology.coordinates.api import (  # type: ignore[import]
        AbstractCoordinate,
        CrdT,
    )


###############################################################################
# PARAMETERS


_COORDINATE_REPRESENTATION_TRANSFORMS: dict[
    tuple[type[AbstractCoordinate[ArrayT]], type[AbstractCoordinate[ArrayT]]],
    Callable[[AbstractCoordinate[ArrayT]], AbstractCoordinate[ArrayT]],
] = {}


###############################################################################
# EXCEPTIONS


class CoordinateRepresentationoTransformError(Exception):
    """The CoordinateRepresentationo transform error."""


class CoordinateRepresentationTransformNotImplementedError(
    CoordinateRepresentationoTransformError,
):
    """The CoordinateRepresentationo transform not implemented error."""


###############################################################################
# FUNCTIONS


def represent_as(
    from_coordinate: AbstractCoordinate[ArrayT],
    to_coordinate: type[CrdT],
) -> CrdT:
    """Represent the cosmology as a CoordinateRepresentationo.

    Parameters
    ----------
    from_coordinate : AbstractCoordinate[ArrayT]
        The CoordinateRepresentationo to represent the cosmology as.
    to_coordinate : type[AbstractCoordinate[ArrayT]]
        The CoordinateRepresentationo class to transform to.

    Returns
    -------
    AbstractCoordinate[ArrayT]
        The cosmology represented as a CoordinateRepresentationo.
    """
    key = (type(from_coordinate), to_coordinate)
    if key not in _COORDINATE_REPRESENTATION_TRANSFORMS:
        msg = f"there is no registered transform from {key[0].__name__} to {key[1].__name__}"  # noqa: E501
        raise CoordinateRepresentationTransformNotImplementedError(msg)

    return cast(
        "CrdT",
        _COORDINATE_REPRESENTATION_TRANSFORMS[key](
            from_coordinate,
        ),
    )


def register_representation_transform(
    from_coordinate_type: type[AbstractCoordinate[ArrayT]],
    to_coordinate: type[AbstractCoordinate[ArrayT]],
) -> Callable[
    [Callable[[AbstractCoordinate[ArrayT]], AbstractCoordinate[ArrayT]]],
    Callable[[AbstractCoordinate[ArrayT]], AbstractCoordinate[ArrayT]],
]:
    """Register a CoordinateRepresentationo transform.

    Parameters
    ----------
    from_coordinate_type : type[AbstractCoordinate[ArrayT]]
        The CoordinateRepresentationo class to transform from.
    to_coordinate : type[AbstractCoordinate[ArrayT]]
        The CoordinateRepresentationo class to transform to.

    Returns
    -------
    Callable
        The decorator.
    """

    def decorator(
        func: Callable[[AbstractCoordinate[ArrayT]], AbstractCoordinate[ArrayT]],
    ) -> Callable[[AbstractCoordinate[ArrayT]], AbstractCoordinate[ArrayT]]:
        """Registration decorator."""
        _COORDINATE_REPRESENTATION_TRANSFORMS[
            from_coordinate_type,
            to_coordinate,
        ] = func
        return func

    return decorator
