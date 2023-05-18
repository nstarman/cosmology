"""The Cosmology library."""

from __future__ import annotations

from functools import singledispatch

from cosmology.api import HasPhotonComponent
from cosmology.api._array_api import ArrayT

__all__: list[str] = []


def omega_photon0(cosmo: HasPhotonComponent[ArrayT], /) -> ArrayT:
    """Omega photon; the effective radiation density/critical density at z=0."""
    return cosmo.Omega_gamma0


@singledispatch
def rho_photon0(cosmo: HasPhotonComponent[ArrayT], /) -> ArrayT:
    """Photon density at z = 0 in Msol Mpc-3."""
    return cosmo.Omega_gamma0 * cosmo.critical_density0


def omega_photon(cosmo: HasPhotonComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent photon density parameter.

    Parameters
    ----------
    cosmo : HasPhotonComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_gamma(z)


@singledispatch
def rho_photon(cosmo: HasPhotonComponent[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent photon density in Msol Mpc-3.

    Parameters
    ----------
    cosmo : HasPhotonComponent, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Omega_gamma(z) * cosmo.critical_density(z)
