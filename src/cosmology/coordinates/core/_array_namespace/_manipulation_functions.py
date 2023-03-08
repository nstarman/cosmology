"""The Cosmology coordinates library."""

from __future__ import annotations

from functools import singledispatch
from typing import TYPE_CHECKING, Any

__all__: list[str] = []

if TYPE_CHECKING:
    from cosmology.api._array_api import ArrayT

    from .. import AbstractCoordinate  # noqa: TID252


@singledispatch
def broadcast_to(x: Any, /, shape: tuple[int, ...]) -> AbstractCoordinate[ArrayT]:
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
    raise NotImplementedError
