"""The Cosmology coordinates library."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NoReturn, Protocol, TypeVar

from cosmology.api._array_api import ArrayT_co

__all__: list[str] = []

if TYPE_CHECKING:
    from collections.abc import (
        Callable,  # noqa: TCH004, RUF100
        Iterator,
    )

    from cosmology.coordinates.api._base import CrdT  # type: ignore[import]
    from numpy.typing import NDArray  # noqa: TCH004, RUF100


Self = TypeVar("Self", bound="AbstractCoordinate[ArrayT_co]")  # type: ignore[valid-type]  # noqa: E501


class AbstractCoordinate(Protocol[ArrayT_co]):
    """The Cosmology API for coordinates."""

    def __field_array_namespace__(self, /, *, api_version: str | None = None) -> Any:
        """Return the array namespace of the coordinate's fields.

        Returns
        -------
        Any
        """
        ...

    def represent_as(self, representation_type: type[CrdT], /) -> CrdT:
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
        ...

    def __iter__(self: Self) -> Iterator[AbstractCoordinate[ArrayT_co]]:
        """Return an iterator over the coordinates."""
        ...

    def __getitem__(self, key: Any) -> AbstractCoordinate[ArrayT_co]:
        ...

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
        return NotImplemented

    def __ne__(self, other: Any) -> Any:
        """Rich comparison operators are not implemented."""
        return NotImplemented

    def __gt__(self, other: Any) -> NoReturn:
        """Rich comparison operators are not implemented."""
        raise NotImplementedError

    def __ge__(self, other: Any) -> NoReturn:
        """Rich comparison operators are not implemented."""
        raise NotImplementedError

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
        ...

    # ---------------------------
    # Array-API Methods

    def __array_namespace__(self) -> Any:
        """Return the array namespace of the coordinate.

        Returns
        -------
        Any
        """
        ...

    @property
    def ndim(self) -> int:
        """Return the number of dimensions of the broadcasted representation.

        Returns
        -------
        int
            The number of dimensions of the broadcasted representation.
        """
        ...

    @property
    def shape(self) -> tuple[int, ...]:
        """Return the shape of the broadcasted representation.

        Returns
        -------
        tuple[int, ...]
            The broadcasted shape of the representation.
        """
        ...

    @property
    def size(self) -> int:
        """Return the size of the broadcasted representation.

        Returns
        -------
        int
            The size of the broadcasted representation.
        """
        ...

    # ---------------------------
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
        ...

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
        ...

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
        ...
