"""Reentry dynamics module. 3-DOF ballistic reentry with atmospheric drag
and convective heating (Sutton-Graves approximation).
State: [altitude_m, velocity_mps, flight_path_angle_rad]"""

from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp
from typing import Tuple
from ..constants import R_EARTH, G0, R_N_TYPICAL
from .atmosphere import AtmosphereModel

class ReentryModel:
    """Ballistic reentry simulator with heating."""

    def __init__(self):
        self.atm = AtmosphereModel()

    def _reentry_ode(
        self, t: float, y: np.ndarray, mass: float, ref_area: float, cd: float
    ) -> np.ndarray:
        """3DOF equations of motion for ballistic entry."""
        alt, vel, gamma = y
        if alt < 0:
            return np.zeros(3)
        rho = self.atm.get_density(alt)
        r = R_EARTH + alt
        g = G0 * (R_EARTH / r) ** 2
        drag_accel = 0.5 * rho * vel**2 * cd * ref_area / mass
        d_alt = vel * np.sin(gamma)
        d_vel = -drag_accel - g * np.sin(gamma)
        d_gamma = (vel / r - g / vel) * np.cos(gamma) if vel > 1e-3 else 0.0
        return np.array([d_alt, d_vel, d_gamma])

    def simulate_ballistic(
        self,
        alt0: float,
        vel0: float,
        gamma0: float,
        mass: float,
        ref_area: float,
        cd: float,
        t_span: Tuple[float, float] = (0.0, 2000.0),
        rtol: float = 1e-8,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Integrate reentry trajectory. Returns (t, states)."""
        y0 = np.array([alt0, vel0, gamma0], dtype=float)
        sol = solve_ivp(
            lambda t, y: self._reentry_ode(t, y, mass, ref_area, cd),
            t_span,
            y0,
            method="DOP853",
            rtol=rtol,
            atol=1e-9,
            events=lambda t, y: y[0],  # stop at alt=0
        )
        return sol.t, sol.y.T

    def convective_heat_rate(
        self, velocity: float, altitude: float, nose_radius: float = R_N_TYPICAL
    ) -> float:
        """Sutton-Graves convective heating rate [W/m²]."""
        rho = self.atm.get_density(altitude)
        # Classic form: q = k * sqrt(rho / R_n) * V^3.15
        k = 1.83e-4  # empirical constant SI
        return k * np.sqrt(rho / nose_radius) * (velocity ** 3.15)