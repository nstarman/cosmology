"""The cosmological coordinates API standard."""


from dataclasses import dataclass

from cosmology.coordinates.api.frame._base import CoordinateFrame as CoordinateFrameAPI

__all__: list[str] = []


@dataclass
class CoordinateFrame(CoordinateFrameAPI):
    """The API for Coordinate Frames.

    Parameters
    ----------
    name : str
        The name of the frame.
    frame_fields : tuple[str, ...]
        The names of the fields in the frame.

    default_representations : tuple[type[CoordinateRepresentation], ...] | None
        The default representations for the frame.
        If `None` (default), use the current representation types.
    """

    name: str
    frame_fields: tuple[str, ...]
