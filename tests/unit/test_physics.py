"""Unit tests for core physics modules. Run with pytest."""

import numpy as np
import pytest
from src.blackvector.core.constants import MU_EARTH, R_EARTH, G0
from src.blackvector.core.physics.orbital import TwoBodyPropagator
from src.blackvector.core.physics.atmosphere import AtmosphereModel
from src.blackvector.core.physics.propulsion import RocketPropulsion, PropulsionConfig
from src.blackvector.core.physics.reentry import ReentryModel

def test_vis_viva_leo():
    prop = TwoBodyPropagator()
    # LEO ~400km, v ~7660 m/s
    v = prop.vis_viva(R_EARTH + 400_000, R_EARTH + 400_000)
    assert 7600 < v < 7800

def test_atmosphere_sea_level():
    atm = AtmosphereModel()
    t, p, rho = atm.get_conditions(0.0)
    assert 287 < t < 289
    assert 101000 < p < 102000
    assert 1.22 < rho < 1.23

def test_tsiolkovsky():
    cfg = PropulsionConfig(isp=300, propellant_mass=9000, dry_mass=1000, thrust=50000, burn_time=180)
    rocket = RocketPropulsion(cfg)
    dv = rocket.tsiolkovsky_delta_v()
    assert dv > 7000  # realistic for stage

def test_reentry_runs():
    reentry = ReentryModel()
    t, states = reentry.simulate_ballistic(120_000, 7800, -0.4, 3000, 8.0, 1.3, (0, 600))
    assert len(t) > 10
    assert states[-1, 0] < 1000  # reached low altitude

def test_propagate_orbit():
    prop = TwoBodyPropagator()
    r0 = np.array([R_EARTH + 400_000, 0, 0])
    v0 = np.array([0, np.sqrt(MU_EARTH / (R_EARTH + 400_000)), 0])
    t, states = prop.propagate(r0, v0, (0, 1000))
    assert len(t) > 5
    # Energy roughly conserved
    energy0 = 0.5 * np.linalg.norm(v0)**2 - MU_EARTH / np.linalg.norm(r0)
    energyf = 0.5 * np.linalg.norm(states[-1,3:])**2 - MU_EARTH / np.linalg.norm(states[-1,:3])
    assert abs(energyf - energy0) < 100  # loose tolerance for short arc