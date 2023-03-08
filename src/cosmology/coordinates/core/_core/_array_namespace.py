"""The Cosmology coordinates library."""

from __future__ import annotations

import functools
import operator
from typing import TYPE_CHECKING, cast

from cosmology.coordinates.core._array_namespace import broadcast_to, equal, not_equal
from cosmology.coordinates.core._core._core import BaseCoordinate

__all__: list[str] = []

if TYPE_CHECKING:
    from cosmology.api._array_api import ArrayT


@broadcast_to.register(BaseCoordinate)
def _broadcast_to(
    x: BaseCoordinate[ArrayT],
    /,
    shape: tuple[int, ...],
) -> BaseCoordinate[ArrayT]:
    """Broadcasts an array to a specified shape.

    Parameters
    ----------
    x: array
        array to broadcast.
    shape: Tuple[int, ...]
        array shape. Must be compatible with ``x`` (see :ref:`broadcasting`). If
        the array is incompatible with the specified shape, the function should
        raise an exception.

    Returns
    -------
    out: array
        an array having a specified shape. Must have the same data type as
        ``x``.
    """
    xp = x.__field_array_namespace__()

    return x.__class__(
        **{n: xp.broadcast_to(getattr(x, n), shape) for n in x.array_fields},
    )


@equal.register(BaseCoordinate)
def _equal(x1: BaseCoordinate[ArrayT], x2: BaseCoordinate[ArrayT], /) -> ArrayT:
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
    if not isinstance(x2, type(x1)):
        return NotImplemented

    return cast(
        "ArrayT",
        functools.reduce(
            operator.and_,
            (getattr(x1, n) == getattr(x2, n) for n in x2.array_fields),
        ),
    )


@not_equal.register(BaseCoordinate)
def _not_equal(x1: BaseCoordinate[ArrayT], x2: BaseCoordinate[ArrayT], /) -> ArrayT:
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
    if not isinstance(x2, type(x1)):
        return NotImplemented

    return cast(
        "ArrayT",
        functools.reduce(
            operator.and_,
            (getattr(x1, n) != getattr(x2, n) for n in x2.array_fields),
        ),
    )
