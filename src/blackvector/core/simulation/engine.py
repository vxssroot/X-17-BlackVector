"""Modular simulation engine. Composes dynamics from physics modules
into integrated trajectories. Supports custom dynamics injection for GNC/optimization."""

from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp
from typing import Callable, Any, Tuple, Optional
from pydantic import BaseModel, Field

class SimulationConfig(BaseModel):
    """Engine configuration."""
    method: str = Field("DOP853", description="scipy.integrate.solve_ivp method")
    rtol: float = Field(1e-9, gt=0)
    atol: float = Field(1e-12, gt=0)
    max_step: Optional[float] = Field(None, gt=0)

class SimulationEngine:
    """High-performance, extensible simulation runtime."""

    def __init__(self, config: Optional[SimulationConfig] = None):
        self.config = config or SimulationConfig()

    def run(
        self,
        dynamics: Callable[[float, np.ndarray, Any], np.ndarray],
        state0: np.ndarray,
        t_span: Tuple[float, float],
        args: tuple = (),
        events: Optional[list] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Execute dynamics integration. dynamics(t, y, *args) -> dy/dt"""
        sol = solve_ivp(
            lambda t, y: dynamics(t, y, *args),
            t_span,
            state0.astype(float),
            method=self.config.method,
            rtol=self.config.rtol,
            atol=self.config.atol,
            max_step=self.config.max_step or np.inf,
            events=events,
        )
        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")
        return sol.t, sol.y.T

    def run_reentry(
        self,
        reentry_model,
        alt0: float,
        vel0: float,
        gamma0_rad: float,
        mass: float,
        area: float,
        cd: float,
        t_end: float = 1800.0,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Convenience wrapper for reentry."""
        return reentry_model.simulate_ballistic(
            alt0, vel0, gamma0_rad, mass, area, cd, (0.0, t_end), self.config.rtol
        )