"""US Standard Atmosphere 1976 model (simplified layered implementation).
Provides density, temperature, pressure vs geometric altitude.
Valid 0-86 km. Above uses exponential approximation.
All calculations SI units."""

from __future__ import annotations
import numpy as np
from typing import Tuple
from ..constants import R_EARTH, RHO0_SEA

class AtmosphereModel:
    """Production atmosphere model for drag and reentry calculations."""

    # Layer boundaries (m), lapse rate (K/m), base temp (K), base pressure (Pa)
    LAYERS = [
        (0.0, 11_000.0, -0.0065, 288.15, 101_325.0),
        (11_000.0, 20_000.0, 0.0, 216.65, 22_632.1),
        (20_000.0, 32_000.0, 0.001, 216.65, 5_474.89),
        (32_000.0, 47_000.0, 0.0028, 228.65, 868.019),
        (47_000.0, 51_000.0, 0.0, 270.65, 110.906),
        (51_000.0, 71_000.0, -0.0028, 270.65, 66.9389),
        (71_000.0, 86_000.0, -0.002, 214.65, 3.95642),
    ]

    R = 287.053  # J/(kg·K) specific gas constant for air

    def get_conditions(self, altitude: float) -> Tuple[float, float, float]:
        """Return (temperature_K, pressure_Pa, density_kgm3) at geometric altitude [m]."""
        h = max(0.0, float(altitude))
        for h1, h2, lapse, t0, p0 in self.LAYERS:
            if h1 <= h < h2:
                if abs(lapse) < 1e-12:
                    t = t0
                    p = p0 * np.exp(-9.80665 * (h - h1) / (self.R * t))
                else:
                    t = t0 + lapse * (h - h1)
                    p = p0 * (t / t0) ** (-9.80665 / (lapse * self.R))
                rho = p / (self.R * t)
                return t, p, rho
        # Exosphere approximation above 86 km
        t = 186.8673
        p = 3.95642 * np.exp(-9.80665 * (h - 86_000) / (self.R * t))
        rho = p / (self.R * t)
        return t, p, rho

    def get_density(self, altitude: float) -> float:
        """Density [kg/m³] at altitude [m]."""
        _, _, rho = self.get_conditions(altitude)
        return rho

    def get_mach(self, velocity: float, altitude: float) -> float:
        """Approximate Mach number. Uses local speed of sound."""
        t, _, _ = self.get_conditions(altitude)
        a_sound = np.sqrt(1.4 * self.R * t)  # gamma=1.4 for air
        return velocity / a_sound if a_sound > 0 else 0.0

    def get_drag_coefficient(self, mach: float) -> float:
        """Simple blunt-body Cd vs Mach (approximation for reentry vehicles)."""
        if mach < 0.8:
            return 0.8
        elif mach < 1.2:
            return 0.8 + 0.6 * (mach - 0.8) / 0.4
        elif mach < 5.0:
            return 1.4 - 0.6 * (mach - 1.2) / 3.8
        else:
            return 1.05  # hypersonic plateau