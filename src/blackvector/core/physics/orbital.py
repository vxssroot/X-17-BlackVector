"""Orbital mechanics module. Two-body propagator with high-order integration.
Includes Keplerian element conversion and vis-viva equation.
Extensible for J2, drag, third-body via dynamics injection."""

from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp
from typing import Tuple, Optional
from ..constants import MU_EARTH, R_EARTH, G0

class TwoBodyPropagator:
    """High-fidelity two-body orbital propagator (Cartesian state)."""

    def __init__(self, mu: float = MU_EARTH):
        self.mu = mu

    @staticmethod
    def _two_body_ode(t: float, y: np.ndarray, mu: float) -> np.ndarray:
        """State derivative: [rx,ry,rz, vx,vy,vz] -> velocities + accelerations."""
        r = y[:3]
        r_norm = np.linalg.norm(r)
        if r_norm < R_EARTH * 0.9:
            # Guard against surface impact in propagator
            return np.zeros(6)
        accel = -mu * r / r_norm**3
        return np.concatenate((y[3:6], accel))

    def propagate(
        self,
        r0: np.ndarray,
        v0: np.ndarray,
        t_span: Tuple[float, float],
        rtol: float = 1e-9,
        atol: float = 1e-12,
        method: str = "DOP853",
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Propagate state vector. Returns (t, states) where states shape (N, 6)."""
        y0 = np.concatenate((r0, v0))
        sol = solve_ivp(
            lambda t, y: self._two_body_ode(t, y, self.mu),
            t_span,
            y0,
            method=method,
            rtol=rtol,
            atol=atol,
            dense_output=False,
        )
        if not sol.success:
            raise RuntimeError(f"Propagation failed: {sol.message}")
        return sol.t, sol.y.T

    def vis_viva(self, r: float, a: float) -> float:
        """Vis-viva equation: v = sqrt[ mu (2/r - 1/a) ]"""
        return np.sqrt(self.mu * (2.0 / r - 1.0 / a))

    def orbital_period(self, a: float) -> float:
        """Kepler third law period [s]"""
        return 2 * np.pi * np.sqrt(a**3 / self.mu)

    def state_to_elements(
        self, r: np.ndarray, v: np.ndarray
    ) -> dict:
        """Convert Cartesian state to classical Keplerian elements.
        Returns dict with a, e, i, raan, argp, nu (angles in rad)."""
        r_norm = np.linalg.norm(r)
        v_norm = np.linalg.norm(v)
        h = np.cross(r, v)
        h_norm = np.linalg.norm(h)
        e_vec = (1.0 / self.mu) * (np.cross(v, h) - self.mu * r / r_norm)
        e = np.linalg.norm(e_vec)
        energy = v_norm**2 / 2 - self.mu / r_norm
        a = -self.mu / (2 * energy) if energy < 0 else np.inf
        i = np.arccos(h[2] / h_norm)
        n = np.cross([0, 0, 1], h)
        n_norm = np.linalg.norm(n)
        raan = np.arccos(n[0] / n_norm) if n_norm > 0 else 0.0
        if n[1] < 0:
            raan = 2 * np.pi - raan
        argp = np.arccos(np.dot(n, e_vec) / (n_norm * e)) if e > 1e-8 and n_norm > 0 else 0.0
        if e_vec[2] < 0:
            argp = 2 * np.pi - argp
        nu = np.arccos(np.dot(e_vec, r) / (e * r_norm)) if e > 1e-8 else 0.0
        if np.dot(r, v) < 0:
            nu = 2 * np.pi - nu
        return {"a": a, "e": e, "i": i, "raan": raan, "argp": argp, "nu": nu}