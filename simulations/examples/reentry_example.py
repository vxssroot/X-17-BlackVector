#!/usr/bin/env python3
"""Example: Ballistic reentry of a generic capsule from LEO deorbit."""

import numpy as np
from src.blackvector.core.physics.reentry import ReentryModel
from src.blackvector.core.simulation.engine import SimulationEngine, SimulationConfig

def main():
    engine = SimulationEngine(SimulationConfig(rtol=1e-8))
    reentry = ReentryModel()

    # Typical deorbit from 400km circular, retro burn lowers perigee
    alt0 = 120_000.0   # interface
    vel0 = 7800.0
    gamma0 = -0.4      # rad ~ -23 deg
    mass = 4500.0
    area = 12.0
    cd = 1.3

    print("Running production reentry simulation...")
    t, states = engine.run_reentry(reentry, alt0, vel0, gamma0, mass, area, cd, t_end=900.0)

    final = states[-1]
    peak_heat = max(reentry.convective_heat_rate(states[i,1], states[i,0]) for i in range(len(t)))

    print(f"Trajectory points: {len(t)}")
    print(f"Final altitude: {final[0]:.1f} m")
    print(f"Final velocity: {final[1]:.1f} m/s")
    print(f"Peak heating: {peak_heat:.2e} W/m²")
    print("Example complete. Extend with matplotlib for plots.")

if __name__ == "__main__":
    main()