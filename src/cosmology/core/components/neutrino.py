"""The Cosmology library."""

from __future__ import annotations

from functools import singledispatch

from cosmology.api import HasNeutrinoComponent
from cosmology.api._array_api import ArrayT

__all__: list[str] = []


def omega_neutrino0(cosmo: HasNeutrinoComponent[ArrayT], /) -> ArrayT:
    """Omega neutrino; the effective neutrino density/critical density at z=0."""
    return cosmo.Omega_nu0


@singledispatch
def rho_neutrino0(cosmo: HasNeutrinoComponent[ArrayT], /) -> ArrayT:
    """Neutrino density at z = 0 in Msol Mpc-3."""
    return cosmo.Omega_nu0 * cosmo.critical_density0


def omega_neutrino(cosmo: HasNeutrinoComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent neutrino density parameter.

    Parameters
    ----------
    cosmo : HasNeutrinoComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_nu(z)


@singledispatch
def rho_neutrino(cosmo: HasNeutrinoComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent neutrino density in Msol Mpc-3.

    Parameters
    ----------
    cosmo : HasNeutrinoComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_nu(z) * cosmo.critical_density(z)


def N_eff(cosmo: HasNeutrinoComponent[ArrayT], /) -> ArrayT:
    """Effective number of neutrino species.

    Parameters
    ----------
    cosmo : HasNeutrinoComponent, positional-only
        The cosmology.

    Returns
    -------
    Array
    """
    return cosmo.Neff


def mass_nu(cosmo: HasNeutrinoComponent[ArrayT], /) -> tuple[ArrayT, ...]:
    """Neutrino mass in eV.

    Parameters
    ----------
    cosmo : HasNeutrinoComponent, positional-only
        The cosmology.

    Returns
    -------
    tuple[Array, ...]
        Tuple of neutrino masses in eV.
    """
    return cosmo.m_nu
