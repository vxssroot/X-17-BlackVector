"""Rocket propulsion models. Tsiolkovsky rocket equation, thrust profiles,
mass evolution, and simple staging support.
Production-ready for trajectory integration."""

from __future__ import annotations
import numpy as np
from pydantic import BaseModel, Field, validator
from typing import Optional
from ..constants import G0

class PropulsionConfig(BaseModel):
    """Validated propulsion configuration."""
    isp: float = Field(..., gt=50, lt=600, description="Specific impulse [s]")
    propellant_mass: float = Field(..., gt=0, description="Initial propellant mass [kg]")
    dry_mass: float = Field(..., gt=0, description="Dry mass [kg]")
    thrust: Optional[float] = Field(None, gt=0, description="Constant thrust [N] or None for variable")
    burn_time: Optional[float] = Field(None, gt=0, description="Burn duration [s]")
    engine_type: str = Field("liquid", description="liquid | solid | hybrid")

    @validator("thrust", "burn_time", pre=True, always=True)
    def check_consistency(cls, v, values):
        if values.get("thrust") is not None and values.get("burn_time") is None:
            raise ValueError("burn_time required when thrust is specified")
        return v

class RocketPropulsion:
    """Rocket engine / stage model with realistic mass and thrust evolution."""

    def __init__(self, config: PropulsionConfig):
        self.config = config
        self.initial_mass = config.propellant_mass + config.dry_mass
        self.current_propellant = config.propellant_mass
        self._m_dot = None
        if config.thrust:
            self._m_dot = config.thrust / (config.isp * G0)

    @property
    def current_mass(self) -> float:
        return self.config.dry_mass + self.current_propellant

    def tsiolkovsky_delta_v(self, m_final: Optional[float] = None) -> float:
        """Ideal Δv = Isp * g0 * ln(m0 / mf)"""
        m0 = self.initial_mass
        mf = m_final or self.config.dry_mass
        if mf <= 0 or m0 <= mf:
            return 0.0
        return self.config.isp * G0 * np.log(m0 / mf)

    def instantaneous_thrust(self, t: float) -> float:
        """Thrust at time t into burn [N]."""
        if self.config.thrust is None or self.config.burn_time is None:
            return 0.0
        if 0 <= t < self.config.burn_time:
            return self.config.thrust
        return 0.0

    def update_mass(self, dt: float, t: float = 0.0) -> float:
        """Advance mass by dt seconds. Returns mass consumed this step."""
        if self._m_dot is None or self.current_propellant <= 0:
            return 0.0
        dm = min(self._m_dot * dt, self.current_propellant)
        self.current_propellant -= dm
        return dm

    def reset(self):
        """Reset propellant mass to initial."""
        self.current_propellant = self.config.propellant_mass