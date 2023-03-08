"""The Cosmology coordinates library."""

from dataclasses import dataclass

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.core._core import BaseCoordinate


@dataclass(frozen=True)
class RedshiftRepresentation(BaseCoordinate[ArrayT]):
    """Redshift cosmology representation.

    Parameters
    ----------
    redshift : ArrayT
        Redshift.
    """

    redshift: ArrayT


# @dataclass(frozen=True)
# class CylindricalRepresentation(BaseCoordinate[ArrayT]):
#     """Cylindrical cosmology representation.

#     Parameters
#     ----------
#         Redshift.
#         Cylindrical radius.
#         Cylindrical angle.
#     """


# @dataclass(frozen=True)
# class CartesianRepresentation(BaseCoordinate[ArrayT]):
#     """Cartesian cosmology representation.

#     Parameters
#     ----------
#         Redshift.
#         Cartesian x-coordinate.
#         Cartesian y-coordinate.
#     """


# # Representation transforms


# @register_representation_transform(RedshiftRepresentation, CylindricalRepresentation)
# def _redshift_to_cylindrical(
#     redshift_representation: RedshiftRepresentation[ArrayT],
# ) -> CylindricalRepresentation[ArrayT]:
#     """Convert redshift to cylindrical."""
#     # TODO! or raise RepresentationTransformError
#     return CylindricalRepresentation[ArrayT](


# @register_representation_transform(CylindricalRepresentation, RedshiftRepresentation)
# def _cylindrical_to_redshift(
#     cylindrical_representation: CylindricalRepresentation[ArrayT],
# ) -> RedshiftRepresentation[ArrayT]:
#     """Convert cylindrical to redshift."""
#     return RedshiftRepresentation[ArrayT](


# @register_representation_transform(RedshiftRepresentation, CartesianRepresentation)
# def _redshift_to_cartesian(
#     redshift_representation: RedshiftRepresentation[ArrayT],
# ) -> CartesianRepresentation[ArrayT]:
#     """Convert redshift to cartesian."""
#     # TODO! or raise RepresentationTransformError
#     return CartesianRepresentation[ArrayT](


# @register_representation_transform(CartesianRepresentation, RedshiftRepresentation)
# def _cartesian_to_redshift(
#     cartesian_representation: CartesianRepresentation[ArrayT],
# ) -> RedshiftRepresentation[ArrayT]:
#     """Convert cartesian to redshift."""
#     return RedshiftRepresentation[ArrayT](
