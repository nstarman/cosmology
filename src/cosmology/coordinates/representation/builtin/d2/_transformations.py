"""The Cosmology coordinates library."""

from cosmology.api._array_api import ArrayT
from cosmology.coordinates.representation._transformations import (
    register_representation_transform,
)

from ._cartesian import Cartesian
from ._polar import LogPolar, Polar

# -- Cartestian -> X ----------------------------------------------


@register_representation_transform(Cartesian, Cartesian)
def _c2c(c: Cartesian[ArrayT], /) -> Cartesian[ArrayT]:
    """Convert Cartesian to Cartesian."""
    return c


@register_representation_transform(Cartesian, Polar)
def _c2p(c: Cartesian[ArrayT], /) -> Polar[ArrayT]:
    """Convert Cartesian to Polar."""
    xp = c.__field_array_namespace__()
    rho = (c.x**2 + c.y**2) ** 0.5
    phi = xp.atan2(c.y, c.x)
    return Polar[ArrayT](rho, phi)


@register_representation_transform(Cartesian, LogPolar)
def _c2lp(c: Cartesian[ArrayT], /) -> LogPolar[ArrayT]:
    """Convert Cartesian to Polar."""
    xp = c.__field_array_namespace__()
    logrho = xp.log(c.x**2 + c.y**2) / 2.0
    phi = xp.atan2(c.y, c.x)
    return LogPolar[ArrayT](logrho, phi)


# -- Polar -> X ----------------------------------------------


@register_representation_transform(Polar, Polar)
def _p2p(c: Polar[ArrayT], /) -> Polar[ArrayT]:
    """Convert Polar to Polar."""
    return c


@register_representation_transform(Polar, Cartesian)
def _p2c(c: Polar[ArrayT], /) -> Cartesian[ArrayT]:
    """Convert Polar to Cartesian."""
    xp = c.__field_array_namespace__()
    return Cartesian[ArrayT](x=c.rho * xp.cos(c.phi), y=c.rho * xp.sin(c.phi))


@register_representation_transform(Polar, LogPolar)
def _p2lp(c: Polar[ArrayT], /) -> LogPolar[ArrayT]:
    """Convert Polar to log-polar."""
    xp = c.__field_array_namespace__()
    return LogPolar[ArrayT](rho=xp.log(c.rho), phi=c.phi)


# -- LogPolar -> X ----------------------------------------------


@register_representation_transform(LogPolar, LogPolar)
def _lp2lp(c: LogPolar[ArrayT], /) -> LogPolar[ArrayT]:
    """Convert LogPolar to LogPolar."""
    return c


@register_representation_transform(LogPolar, Cartesian)
def _lp2c(c: LogPolar[ArrayT], /) -> Cartesian[ArrayT]:
    """Convert LogPolar to Cartesian."""
    xp = c.__field_array_namespace__()
    r = xp.exp(c.rho)
    return Cartesian[ArrayT](x=r * xp.cos(c.phi), y=r * xp.sin(c.phi))


@register_representation_transform(LogPolar, Polar)
def _lp2p(c: LogPolar[ArrayT], /) -> Polar[ArrayT]:
    """Convert LogPolar to Polar."""
    xp = c.__field_array_namespace__()
    return Polar[ArrayT](rho=xp.log(c.rho), phi=c.phi)
