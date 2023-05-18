"""The Cosmology library."""

from __future__ import annotations

from functools import singledispatch

from cosmology.api import HasDarkEnergyComponent
from cosmology.api._array_api import ArrayT

__all__: list[str] = []


def omega_de0(cosmo: HasDarkEnergyComponent[ArrayT], /) -> ArrayT:
    """Omega dark energy; the effective dark energy density/critical density at z=0."""
    return cosmo.Omega_de0


@singledispatch
def rho_de0(cosmo: HasDarkEnergyComponent[ArrayT], /) -> ArrayT:
    """Dark energy density at z = 0 in Msol Mpc-3."""
    return cosmo.Omega_de0 * cosmo.critical_density0


def omega_de(cosmo: HasDarkEnergyComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent dark energy density parameter.

    Parameters
    ----------
    cosmo : HasDarkEnergyComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_de(z)


@singledispatch
def rho_de(cosmo: HasDarkEnergyComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent dark energy density in Msol Mpc-3.

    Parameters
    ----------
    cosmo : HasDarkEnergyComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_de(z) * cosmo.critical_density(z)
