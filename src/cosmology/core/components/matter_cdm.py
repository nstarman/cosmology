"""The Cosmology library."""

from __future__ import annotations

from functools import singledispatch

from cosmology.api import HasDarkMatterComponent
from cosmology.api._array_api import ArrayT

__all__: list[str] = []


def omega_dm0(cosmo: HasDarkMatterComponent[ArrayT], /) -> ArrayT:
    """Omega dark matter; the effective dark matter density/critical density at z=0."""
    return cosmo.Omega_dm0


@singledispatch
def rho_dm0(cosmo: HasDarkMatterComponent[ArrayT], /) -> ArrayT:
    """Dark matter density at z = 0 in Msol Mpc-3."""
    return cosmo.Omega_dm0 * cosmo.critical_density0


def omega_dm(cosmo: HasDarkMatterComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent dark matter density parameter.

    Parameters
    ----------
    cosmo : HasDarkMatterComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_dm(z)


@singledispatch
def rho_dm(cosmo: HasDarkMatterComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent dark matter density in Msol Mpc-3.

    Parameters
    ----------
    cosmo : HasDarkMatterComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_dm(z) * cosmo.critical_density(z)
