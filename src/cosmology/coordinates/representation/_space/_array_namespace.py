"""The Cosmology coordinates library."""

from __future__ import annotations

import functools
import operator
from typing import TYPE_CHECKING, TypeVar, cast

from cosmology.coordinates.representation._space._core import CoordinateSpace
from cosmology.coordinates.representation.array_namespace import (
    broadcast_to,
    equal,
    not_equal,
)

__all__: list[str] = []

if TYPE_CHECKING:
    from cosmology.api._array_api import ArrayT

K = TypeVar("K")


@broadcast_to.register(CoordinateSpace)
def _broadcast_to(
    x: CoordinateSpace[K, ArrayT],
    /,
    shape: tuple[int, ...],
) -> CoordinateSpace[K, ArrayT]:
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
    xp = x.__array_namespace__()
    return x.__class__(
        {k: xp.broadcast_to(v, shape) for k, v in x.items()},
    )


@equal.register(CoordinateSpace)
def _equal(x1: CoordinateSpace[K, ArrayT], x2: CoordinateSpace[K, ArrayT], /) -> ArrayT:
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
    if not isinstance(x2, type(x1)) or x1.keys() != x2.keys():
        return NotImplemented

    return cast(
        "ArrayT",
        functools.reduce(
            operator.and_,
            (x1.__array_namespace__().equal(x1[k], v) for k, v in x2.items()),
        ),
    )


@not_equal.register(CoordinateSpace)
def _not_equal(
    x1: CoordinateSpace[K, ArrayT],
    x2: CoordinateSpace[K, ArrayT],
    /,
) -> ArrayT:
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
    if not isinstance(x2, type(x1)) or x1.keys() != x2.keys():
        return NotImplemented

    return cast(
        "ArrayT",
        functools.reduce(
            operator.and_,
            (x1.__array_namespace__().not_equal(x1[k], v) for k, v in x2.items()),
        ),
    )
