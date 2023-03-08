"""The Cosmology coordinates library."""

from __future__ import annotations

from functools import singledispatch
from typing import TYPE_CHECKING

__all__: list[str] = []

if TYPE_CHECKING:
    from cosmology.api._array_api import ArrayT

    from .. import AbstractCoordinate  # noqa: TID252


@singledispatch
def equal(
    x1: AbstractCoordinate[ArrayT],
    x2: AbstractCoordinate[ArrayT],
) -> AbstractCoordinate[ArrayT]:
    r"""Equality.

    Computes the truth value of ``x1_i == x2_i`` for each element ``x1_i`` of
    the input array ``x1`` with the respective element ``x2_i`` of the input
    array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. May have any data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see
        :ref:`broadcasting`). May have any data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must
        have a data type of ``bool``.
    """
    raise NotImplementedError


@singledispatch
def not_equal(
    x1: AbstractCoordinate[ArrayT],
    x2: AbstractCoordinate[ArrayT],
) -> AbstractCoordinate[ArrayT]:
    r"""Inequality.

    Computes the truth value of ``x1_i != x2_i`` for each element ``x1_i`` of
    the input array ``x1`` with the respective element ``x2_i`` of the input
    array ``x2``.

    Parameters
    ----------
    x1: array
        first input array. May have any data type.
    x2: array
        second input array. Must be compatible with ``x1`` (see
        :ref:`broadcasting`). May have any data type.

    Returns
    -------
    out: array
        an array containing the element-wise results. The returned array must
        have a data type of ``bool``.
    """
    raise NotImplementedError
