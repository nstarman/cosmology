"""The Cosmology coordinates library."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, Any, Callable, NoReturn, TypeVar, cast

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.core._array_namespace._utils import get_namespace
from cosmology.coordinates.core._base import AbstractCoordinate
from cosmology.coordinates.core._transformations import represent_as

__all__: list[str] = []

if TYPE_CHECKING:
    from collections.abc import Iterator

    from numpy.typing import NDArray  # noqa: TCH004, RUF100


CrdT = TypeVar("CrdT", bound="BaseCoordinate[ArrayT]")  # type: ignore[valid-type]


@dataclass(frozen=True, eq=False)
class BaseCoordinate(AbstractCoordinate[ArrayT]):
    """Base class for cosmology representations.

    Parameters
    ----------
    redshift : ArrayT
        Redshift.
    """

    def __post_init__(self) -> None:
        self._array_fields_: tuple[str, ...]
        object.__setattr__(
            self,
            "_array_fields_",
            tuple(
                f.name
                for f in fields(self)
                if hasattr(getattr(self, f.name), "__array_namespace__")
            ),
        )

        # Broadcast the fields to a uniform shape.
        xp = self.__field_array_namespace__()
        arrs: tuple[ArrayT, ...] = xp.broadcast_arrays(
            *(getattr(self, n) for n in self._array_fields_),
        )
        for n, arr in zip(self._array_fields_, arrs):
            object.__setattr__(self, n, arr)

    @property
    def array_fields(self) -> tuple[str, ...]:
        """The fields that are arrays."""
        return self._array_fields_

    def __field_array_namespace__(self, /, *, api_version: str | None = None) -> Any:
        return get_namespace(
            *(getattr(self, f) for f in self._array_fields_),
            api_version=api_version,
        )

    def represent_as(self, representation_type: type[CrdT], /) -> CrdT:
        """Represent as a different representation.

        Parameters
        ----------
        representation_type : type, positional-only
            Representation class to transform to.

        Returns
        -------
        BaseRepresentation
            Representation object of type ``representation_type``.
        """
        return cast("CrdT", represent_as(self, representation_type))

    # ---------------------------
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
        return int(getattr(self, self._array_fields_[0]).shape[0])

    def __iter__(self: CrdT) -> Iterator[CrdT]:
        """Return an iterator over the coordinates."""
        yield from (self[i] for i in range(len(self)))

    def __getitem__(self: CrdT, item: int | slice) -> CrdT:
        """Return a selection from the broadcasted Representation.

        Parameters
        ----------
        item : int or slice
            The item to apply to the fields.

        Returns
        -------
        Coordinate
            A new representation with the item applied to the fields.
        """
        return self.__class__(
            **{f: getattr(self, f)[item] for f in self._array_fields_},
        )

    # =============================================================
    # Array-API Methods

    def __array_namespace__(self, /, *, api_version: str | None = None) -> Any:
        from cosmology.coordinates.core import _array_namespace

        return _array_namespace

    @property
    def ndim(self) -> int:
        """Return the number of dimensions of the broadcasted representation.

        Returns
        -------
        int
            The number of dimensions of the broadcasted representation.
        """
        return int(getattr(self, self._array_fields_[0]).ndim)

    @property
    def shape(self) -> tuple[int, ...]:
        """Return the shape of the broadcasted representation.

        Returns
        -------
        tuple[int, ...]
            The broadcasted shape of the representation.
        """
        return cast(tuple[int, ...], getattr(self, self._array_fields_[0]).shape)

    @property
    def size(self) -> int:
        """Return the size of the broadcasted representation.

        Returns
        -------
        int
            The size of the broadcasted representation.
        """
        return int(getattr(self, self._array_fields_[0]).size)

    # ========================================================================
    # Rich comparison

    def __lt__(self, other: Any) -> NoReturn:
        """Rich comparison operators are not implemented."""
        raise NotImplementedError

    def __le__(self, other: Any) -> NoReturn:
        """Rich comparison operators are not implemented."""
        raise NotImplementedError

    def __eq__(self, other: Any) -> Any:
        """Rich comparison operators are not implemented."""
        if not isinstance(other, type(self)):
            return NotImplemented

        return all(getattr(self, n) == getattr(other, n) for n in other.array_fields)

    def __ne__(self, other: Any) -> Any:
        """Rich comparison operators are not implemented."""
        if not isinstance(other, type(self)):
            return NotImplemented

        return all(getattr(self, n) != getattr(other, n) for n in other.array_fields)

    def __gt__(self, other: Any) -> NoReturn:
        """Rich comparison operators are not implemented."""
        raise NotImplementedError

    def __ge__(self, other: Any) -> NoReturn:
        """Rich comparison operators are not implemented."""
        raise NotImplementedError

    # ========================================================================
    # Numpy Compatibility Methods

    def __array__(self, dtype: Any = None) -> NDArray[Any]:
        """Return a numpy array from the representation.

        Parameters
        ----------
        dtype : Any, optional
            The dtype of the returned array. If not provided, the dtype is
            inferred from the representation.

        Returns
        -------
        Any
            Numpy array.
        """
        import numpy as np

        dtype = [(f.name, np.dtype(getattr(self, f.name))) for f in fields(self)]

        out = np.empty(self.shape, dtype=dtype)
        for f in fields(self):
            out[f.name] = getattr(self, f.name)

        return out

    def __array_ufunc__(
        self,
        ufunc: Callable[..., Any],
        method: str,
        *inputs: Any,
        **kwargs: Any,
    ) -> Any:
        """Return the result of the ufunc on the representation.

        Parameters
        ----------
        ufunc : Callable[..., Any]
            The ufunc to apply.
        method : str
            The method to apply.
        *inputs : Any
            The inputs to apply the ufunc to.
        **kwargs : Any
            The keyword arguments to apply to the ufunc.

        Returns
        -------
        Any
            The result of the ufunc.
        """
        raise NotImplementedError

    def __array_function__(
        self,
        func: Callable[..., Any],
        types: tuple[type, ...],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        """Return the result of the function on the representation.

        Parameters
        ----------
        func : Callable[..., Any]
            The function to apply.
        types : tuple[type, ...]
            The types to apply the function to.
        args : tuple[Any, ...]
            The arguments to apply to the function.
        kwargs : dict[str, Any]
            The keyword arguments to apply to the function.

        Returns
        -------
        Any
            The result of the function.
        """
        raise NotImplementedError
