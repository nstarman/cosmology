"""The Cosmology coordinates library."""

from cosmology.coordinates.representation import builtin
from cosmology.coordinates.representation._base._base import CoordinateRepresentation
from cosmology.coordinates.representation._space._core import CoordinateSpace
from cosmology.coordinates.representation._transformations import (
    register_representation_transform,
    to_coordinate_representation,
)

__all__ = [
    "builtin",
    # functions
    "to_coordinate_representation",
    "register_representation_transform",
    # classes
    "CoordinateRepresentation",
    "CoordinateSpace",
]

# Register the dispatch functions
