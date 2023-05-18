"""The Cosmology coordinates library."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.api.representation._base import ArrayCoordinateRepresentation
from cosmology.coordinates.representation import array_namespace
from cosmology.coordinates.representation._transformations import (
    to_coordinate_representation,
)
from cosmology.coordinates.representation.array_namespace._utils import (
    get_fields_namespace,
)

__all__: list[str] = []

if TYPE_CHECKING:
    from collections.abc import Iterator

    from cosmology.coordinates.api.representation._transformations import (
        CoordinateRepresentationTransformationRegistry,
    )
    from numpy.typing import NDArray  # noqa: TCH004, RUF100


CrdT = TypeVar("CrdT", bound="CoordinateRepresentation[ArrayT]")  # type: ignore[valid-type]  # noqa: E501


@dataclass(frozen=True, eq=False)
class CoordinateRepresentation(ArrayCoordinateRepresentation[ArrayT]):
    """Base class for cosmology representations.

    Parameters
    ----------
    redshift : ArrayT
        Redshift.
    """

    def __post_init__(self) -> None:
        self._coordinate_fields_: tuple[str, ...]
        object.__setattr__(
            self,
            "_coordinate_fields_",
            tuple(
                f.name
                for f in fields(self)
                if hasattr(getattr(self, f.name), "__array_namespace__")
            ),
        )

        # Broadcast the fields to a uniform shape.
        xp = self.__field_array_namespace__()
        arrs: tuple[ArrayT, ...] = xp.broadcast_arrays(
            *(getattr(self, n) for n in self._coordinate_fields_),
        )
        for n, arr in zip(self._coordinate_fields_, arrs):
            object.__setattr__(self, n, arr)

    @property
    def coordinate_fields(self) -> tuple[str, ...]:
        """The fields that are arrays."""
        return self._coordinate_fields_

    def to_coordinate_representation(
        self,
        representation_type: type[CrdT],
        /,
        *coordinates: CoordinateRepresentation[ArrayT],
        representation_registry: CoordinateRepresentationTransformationRegistry[ArrayT]
        | None = None,
    ) -> CrdT:
        """Return the coordinate in a new representation.

        Parameters
        ----------
        representation_type : type, positional-only
            Coordinate class to transform to.

        *coordinates : Coordinate, optional
            Additional coordinates required to transform to the new
            representation, e.g. differentials require a position coordinate.

        representation_registry : CoordinateRepresentationTransformationRegistry, optional
            Registry of representation transformations.
            If `None` (default), use the default global registry.

        Returns
        -------
        Coordinate
            Coordinate object of type ``representation_type``.
        """  # noqa: E501
        return to_coordinate_representation(
            self,
            representation_type,
            *coordinates,
            representation_registry=representation_registry,
        )

    # =============================================================
    # Emulating container types

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
            **{f: getattr(self, f)[item] for f in self.coordinate_fields},
        )

    def __len__(self) -> int:
        """Return the length of the coordinate.

        The fields of the coordinate can have different lengths, but should
        be broadcastable to a uniform shape. This method returns the length of
        that broadcasted fields.

        Returns
        -------
        int
        """
        return int(getattr(self, self.coordinate_fields[0]).shape[0])

    def __iter__(self: CrdT) -> Iterator[CrdT]:
        """Return an iterator over the coordinates."""
        yield from (self[i] for i in range(len(self)))

    # =============================================================
    # Coordinate Array-API Methods

    def __field_array_namespace__(self, /, *, api_version: str | None = None) -> Any:
        return get_fields_namespace(
            *(getattr(self, f) for f in self._coordinate_fields_),
            api_version=api_version,
        )

    # =============================================================
    # Array-API Methods

    def __array_namespace__(self, /, *, api_version: str | None = None) -> Any:
        return array_namespace

    @property
    def ndim(self) -> int:
        """Return the number of dimensions of the broadcasted representation.

        Returns
        -------
        int
            The number of dimensions of the broadcasted representation.
        """
        return int(getattr(self, self.coordinate_fields[0]).ndim)

    @property
    def shape(self) -> tuple[int, ...]:
        """Return the shape of the broadcasted representation.

        Returns
        -------
        tuple[int, ...]
            The broadcasted shape of the representation.
        """
        return cast(tuple[int, ...], getattr(self, self.coordinate_fields[0]).shape)

    @property
    def size(self) -> int:
        """Return the size of the broadcasted representation.

        Returns
        -------
        int
            The size of the broadcasted representation.
        """
        return int(getattr(self, self.coordinate_fields[0]).size)

    # ========================================================================
    # Rich comparison

    def __eq__(self, other: Any) -> Any:
        """Rich comparison operators are not implemented."""
        if not isinstance(other, type(self)):
            return NotImplemented

        return all(
            getattr(self, n) == getattr(other, n) for n in other.coordinate_fields
        )

    def __ne__(self, other: Any) -> Any:
        """Rich comparison operators are not implemented."""
        if not isinstance(other, type(self)):
            return NotImplemented

        return all(
            getattr(self, n) != getattr(other, n) for n in other.coordinate_fields
        )

    # ========================================================================
    # Numpy Compatibility Methods

    def __array__(self, dtype: Any = None) -> NDArray[Any]:
        """Return a numpy array from the representation.

        Parameters
        ----------
        dtype : Any, optional
            The dtype of each field of the returned array. If not provided, the
            dtype is inferred from the representation.

        Returns
        -------
        ndarray
            structured Numpy array.
        """
        import numpy as np

        dtype = [
            (f.name, dtype if dtype is not None else np.dtype(getattr(self, f.name)))
            for f in fields(self)
        ]

        out = np.empty(self.shape, dtype=dtype)
        for f in fields(self):
            out[f.name] = getattr(self, f.name)

        return out

    def __array_ufunc__(
        self, ufunc: Callable[..., Any], method: str, *inputs: Any, **kwargs: Any
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
