"""The Cosmology library."""

from __future__ import annotations

from cosmology.api import StandardCosmology
from cosmology.api._array_api import ArrayT

__all__: list[str] = []


def hubble_parameter0(cosmo: StandardCosmology[ArrayT], /) -> ArrayT:
    """Hubble parameter at z=0."""
    return cosmo.H0


def dimensionless_hubble_parameter0(cosmo: StandardCosmology[ArrayT], /) -> ArrayT:
    """Dimensionless Hubble parameter at z=0."""
    return cosmo.h


def hubble_distance(cosmo: StandardCosmology[ArrayT], /) -> ArrayT:
    """Hubble distance in Mpc."""
    return cosmo.hubble_distance


def hubble_time(cosmo: StandardCosmology[ArrayT], /) -> ArrayT:
    """Hubble time in Gyr."""
    return cosmo.hubble_time


def hubble_parameter(cosmo: StandardCosmology[ArrayT], z: ArrayT, /) -> ArrayT:
    """Hubble function :math:`H(z)` in km s-1 Mpc-1.

    Parameters
    ----------
    cosmo : StandardCosmology, positional-only
        The cosmology.
    z : Array
        The redshift(s) at which to evaluate the Hubble parameter.

    Returns
    -------
    Array
    """
    return cosmo.H(z)


def standardized_hubble_function(
    cosmo: StandardCosmology[ArrayT],
    z: ArrayT,
    /,
) -> ArrayT:
    """Standardised Hubble function :math:`E(z) = H(z)/H_0`.

    Parameters
    ----------
    cosmo : StandardCosmology, positional-only
        The cosmology.
    z : Array
        The redshift(s) at which to evaluate efunc.

    Returns
    -------
    Array
    """
    return cosmo.efunc(z)


def inv_standardized_hubble_function(
    cosmo: StandardCosmology[ArrayT],
    z: ArrayT,
    /,
) -> ArrayT:
    """Inverse of ``efunc``.

    Parameters
    ----------
    cosmo : StandardCosmology, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.inv_efunc(z)


# ----------------------------------------------
# Temperature


def Tcmb0(cosmo: StandardCosmology[ArrayT], /) -> ArrayT:
    """CMB temperature at z = 0 in K."""
    return cosmo.Tcmb0


def Tcmb(cosmo: StandardCosmology[ArrayT], z: ArrayT, /) -> ArrayT:
    """Redshift-dependent CMB temperature in K.

    Parameters
    ----------
    cosmo : StandardCosmology, positional-only
        The cosmology.
    z : Array, positional-only
        Input redshift.

    Returns
    -------
    Array
    """
    return cosmo.Tcmb(z)
