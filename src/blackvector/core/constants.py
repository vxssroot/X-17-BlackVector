"""Physical and astronomical constants. All values in SI units unless noted.
Sources: IERS, NASA JPL, US Standard Atmosphere 1976."""

from typing import Final

# Earth
MU_EARTH: Final[float] = 3.986004418e14  # m^3/s^2  GM
R_EARTH: Final[float] = 6378137.0         # m equatorial
R_EARTH_MEAN: Final[float] = 6371000.0    # m mean
OMEGA_EARTH: Final[float] = 7.292115e-5   # rad/s
G0: Final[float] = 9.80665                # m/s^2 standard gravity
J2_EARTH: Final[float] = 1.08263e-3       # J2 perturbation coeff

# Sun
MU_SUN: Final[float] = 1.3271244e20       # m^3/s^2

# Universal
G: Final[float] = 6.67430e-11             # m^3 kg^-1 s^-2
C: Final[float] = 299792458.0             # m/s

# Atmosphere reference
RHO0_SEA: Final[float] = 1.225            # kg/m^3 sea level
SCALE_HEIGHT: Final[float] = 8500.0       # m approximate

# Reentry reference
R_N_TYPICAL: Final[float] = 0.5           # m nose radius for heating calc