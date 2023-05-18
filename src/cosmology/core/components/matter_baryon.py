"""The Cosmology library."""

from __future__ import annotations

from functools import singledispatch

from cosmology.api import HasBaryonComponent
from cosmology.api._array_api import ArrayT

__all__: list[str] = []


def omega_baryon0(cosmo: HasBaryonComponent[ArrayT], /) -> ArrayT:
    """Omega baryon; the effective baryon density/critical density at z=0."""
    return cosmo.Omega_b0


@singledispatch
def rho_baryon0(cosmo: HasBaryonComponent[ArrayT], /) -> ArrayT:
    """Baryon density at z = 0 in Msol Mpc-3."""
    return cosmo.Omega_b0 * cosmo.critical_density0


def omega_baryon(cosmo: HasBaryonComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent baryon density parameter.

    Parameters
    ----------
    cosmo : HasBaryonComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_b(z)


@singledispatch
def rho_baryon(cosmo: HasBaryonComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent baryon density in Msol Mpc-3.

    Parameters
    ----------
    cosmo : HasBaryonComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_b(z) * cosmo.critical_density(z)
