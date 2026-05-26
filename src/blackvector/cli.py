"""Command-line interface for BlackVector simulations.
Usage: blackvector-sim reentry --help"""

import argparse
import sys
import numpy as np
from .core.physics.reentry import ReentryModel
from .core.simulation.engine import SimulationEngine, SimulationConfig
from .core.physics.propulsion import RocketPropulsion, PropulsionConfig

def main():
    parser = argparse.ArgumentParser(
        prog="blackvector-sim",
        description="X-17 BlackVector production aerospace simulation CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Reentry command
    reentry_p = subparsers.add_parser("reentry", help="Run ballistic reentry simulation")
    reentry_p.add_argument("--alt", type=float, default=120_000.0, help="Initial altitude [m]")
    reentry_p.add_argument("--vel", type=float, default=7800.0, help="Initial velocity [m/s]")
    reentry_p.add_argument("--gamma", type=float, default=-0.4, help="Flight path angle [rad]")
    reentry_p.add_argument("--mass", type=float, default=5000.0, help="Vehicle mass [kg]")
    reentry_p.add_argument("--area", type=float, default=10.0, help="Reference area [m²]")
    reentry_p.add_argument("--cd", type=float, default=1.2, help="Drag coefficient")
    reentry_p.add_argument("--t-end", type=float, default=1200.0, help="Max sim time [s]")

    # Simple orbit command
    orbit_p = subparsers.add_parser("orbit", help="Propagate circular orbit")
    orbit_p.add_argument("--alt", type=float, default=400_000.0, help="Orbit altitude [m]")
    orbit_p.add_argument("--duration", type=float, default=5400.0, help="Propagation time [s]")

    args = parser.parse_args()

    if args.command == "reentry":
        engine = SimulationEngine(SimulationConfig(rtol=1e-8))
        reentry = ReentryModel()
        t, states = engine.run_reentry(
            reentry, args.alt, args.vel, args.gamma, args.mass, args.area, args.cd, args.t_end
        )
        final = states[-1]
        print(f"Reentry simulation complete. Final state: alt={final[0]:.1f}m, vel={final[1]:.1f}m/s, gamma={final[2]:.4f}rad")
        print(f"Peak heating rate approx: {reentry.convective_heat_rate(final[1], final[0]):.2e} W/m²")
        return 0

    elif args.command == "orbit":
        from .core.physics.orbital import TwoBodyPropagator
        from .core.constants import R_EARTH, MU_EARTH
        prop = TwoBodyPropagator()
        r0 = np.array([R_EARTH + args.alt, 0.0, 0.0])
        v_circ = np.sqrt(MU_EARTH / (R_EARTH + args.alt))
        v0 = np.array([0.0, v_circ, 0.0])
        t, states = prop.propagate(r0, v0, (0.0, args.duration))
        print(f"Orbit propagation complete. Final position: {states[-1, :3]}")
        return 0

    return 1

if __name__ == "__main__":
    sys.exit(main())