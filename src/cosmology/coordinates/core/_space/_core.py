"""Cosmological coordinates base Protocol."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
    overload,
)

from cosmology.api._array_api import ArrayT_co
from cosmology.coordinates.core._base import AbstractCoordinate
from numpy import broadcast_shapes

__all__: list[str] = []

if TYPE_CHECKING:
    from collections.abc import ItemsView, Iterator, KeysView, Mapping, ValuesView

    from cosmology.coordinates.api._base import CrdT  # type: ignore[import]

K = TypeVar("K")


class CoordinateSpace(AbstractCoordinate[ArrayT_co], Generic[K, ArrayT_co]):
    """Cosmological coordinate space."""

    def __init__(self, m: Mapping[K, AbstractCoordinate[ArrayT_co]], /) -> None:
        # TODO! broadcast the coordinates to a uniform shape
        self._m = dict(m)

        # Broadcast the fields to a uniform shape.
        # TODO! not require Numpy for the initial shape broadcast.
        self._shape = broadcast_shapes(*(v.shape for v in self._m.values()))
        xp = self.__array_namespace__()
        for k, v in self._m.items():
            self._m[k] = xp.broadcast_to(v, self._shape)

    @property
    def _k0(self) -> K:
        return next(iter(self._m.keys()))

    # =============================================================
    # Coordinate Protocol

    def __field_array_namespace__(self, /, *, api_version: str | None = None) -> Any:
        """Return the array namespace of the coordinate's fields.

        Returns
        -------
        Any
        """
        return self._m[self._k0].__field_array_namespace__(api_version=api_version)

    def represent_as(self: CrdT, representation_type: type[CrdT], /) -> CrdT:
        """Return the coordinate in a new representation.

        Parameters
        ----------
        representation_type : type, positional-only
            Coordinate class to transform to.

        Returns
        -------
        Coordinate
            Coordinate object of type ``representation_type``.
        """
        return self.__class__(
            {k: v.represent_as(representation_type) for k, v in self._m.items()},
        )

    def __iter__(self) -> Iterator[AbstractCoordinate[ArrayT_co]]:
        """Return an iterator over the coordinates."""
        yield from (self[i] for i in range(len(self)))

    # =============================================================
    # Emulating container types

    def __len__(self) -> int:
        """Return the length of the coordinate.

        The fields of the coordinate can have different lengths, but should
        be broadcastable to a uniform shape. This method returns the length of
        that broadcasted fields.

        Returns
        -------
        int
        """
        return int(self._shape[0])

    @overload
    def __getitem__(self, key: int | slice) -> CoordinateSpace[K, ArrayT_co]:
        ...

    @overload
    def __getitem__(self, key: K) -> AbstractCoordinate[ArrayT_co]:
        ...

    def __getitem__(self, key: K | int | slice) -> AbstractCoordinate[ArrayT_co]:
        """Return a selection from the broadcasted Representation.

        Parameters
        ----------
        key : K
            The key to apply to the fields.

        Returns
        -------
        Coordinate
            A new representation with the item applied to the fields.
        """
        if isinstance(key, str):
            return self._m[key]  # type: ignore[index]

        return self.__class__(
            {k: v[key] for k, v in self._m.items()},
        )

    # =============================================================
    # Mapping Methods
    # Getitem is overloaded above.

    def keys(self) -> KeysView[K]:
        """Return an iterator over the keys."""
        return self._m.keys()

    def values(self) -> ValuesView[AbstractCoordinate[ArrayT_co]]:
        """Return an iterator over the values."""
        return self._m.values()

    def items(self) -> ItemsView[K, AbstractCoordinate[ArrayT_co]]:
        """Return an iterator over the items."""
        return self._m.items()

    def __repr__(self) -> str:
        """Return a string representation of the coordinate."""
        return f"{self.__class__.__name__}({self._m!r})"

    # =============================================================
    # Array-API Methods

    def __array_namespace__(self, /, *, api_version: str | None = None) -> Any:
        from . import _array_namespace

        return _array_namespace
