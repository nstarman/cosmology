from __future__ import annotations

from typing import Any

__all__: list[str] = []

ArrayAPINamespace = Any  # TODO: Replace with the type once the array API has this.


def get_fields_namespace(*xs: Any, api_version: str | None = None) -> ArrayAPINamespace:
    """Get the array API namespace for the given array inputs.

    Parameters
    ----------
    *xs : Any
        Input arrays for which to get the array API namespace.
    api_version : str | None, optional
        The array API version, by default `None`.

    Returns
    -------
    `~array_api._types.ArrayAPINamespace`
        The array API namespace for the given array inputs.

    Raises
    ------
    ValueError
        If none of the inputs are array API conformant.
        If the inputs are from multiple array API namespaces.
    """
    # `xs` contains one or more arrays.
    namespaces = {
        x.__array_namespace__(api_version=api_version)
        for x in xs
        if hasattr(x, "__array_namespace__")
    }

    if not namespaces:
        msg = "Unrecognized array input"
        raise ValueError(msg)
    elif len(namespaces) != 1:
        msg = f"Multiple namespaces for array inputs: {namespaces}"
        raise ValueError(msg)

    return namespaces.pop()
