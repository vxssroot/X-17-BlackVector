"""Typed vehicle and mission configuration models."""

from pydantic import BaseModel, Field
from typing import Optional, Literal
import math

class VehicleConfig(BaseModel):
    """Reusable launch/reentry vehicle specification."""
    name: str = Field(..., min_length=2)
    dry_mass: float = Field(..., gt=0, description="kg")
    propellant_mass: float = Field(..., gt=0, description="kg")
    ref_area: float = Field(..., gt=0, description="reference area m²")
    isp: float = Field(300.0, gt=50, lt=500)
    cd: float = Field(1.0, gt=0.1, lt=3.0)
    nose_radius: float = Field(0.5, gt=0.01)
    engine_type: Literal["liquid", "solid", "hybrid"] = "liquid"

class MissionConfig(BaseModel):
    """Mission parameters."""
    name: str
    target_orbit_alt: Optional[float] = Field(None, gt=100_000)
    reentry_interface_alt: float = Field(120_000.0, gt=50_000)
    initial_velocity: float = Field(..., gt=0)
    flight_path_angle: float = Field(-0.5, ge=-math.pi/2, le=0)  # rad, negative for descent
    payload_mass: float = Field(0.0, ge=0)