# X-17 BlackVector Architecture

**Systems Engineering View**

The platform follows a layered, modular architecture optimized for high-fidelity physics simulation, extensibility, and production reliability.

## Core Layers
1. **Constants & Primitives** (`core/constants.py`): Immutable physical values, single source of truth.
2. **Physics Domain** (`core/physics/`):
   - `orbital.py`: Two-body + extensible dynamics (J2 ready via callback).
   - `atmosphere.py`: US76 layered model for density, Mach, Cd.
   - `propulsion.py`: Tsiolkovsky + time-dependent thrust/mass.
   - `reentry.py`: 3-DOF ballistic + Sutton-Graves heating.
3. **Simulation Runtime** (`core/simulation/engine.py`): Unified `solve_ivp` wrapper with config, events, and convenience methods.
4. **Typed Models** (`models/`): Pydantic validation for VehicleConfig, MissionConfig.
5. **CLI** (`cli.py`): argparse entrypoint for `blackvector-sim reentry|orbit`.

## Integration Points
- Dynamics functions are pure callables: `dy = f(t, y, *args)`.
- Engine is stateless; models hold internal state (e.g., propellant).
- Future: GNC closed-loop, optimization (SciPy), ML surrogate, Rust core via PyO3.

## Data Flow
Mission Config → Vehicle + Propulsion → Engine.run(dynamics) → Trajectory + Heating + Δv metrics → Visualization / Archive.

## Quality Gates
- Type hints + Pydantic throughout.
- pytest unit tests with energy conservation and physical bounds.
- ruff + mypy in CI.
- Deterministic high-order integration (DOP853).

This design enables rapid mission studies while remaining extensible to 6-DOF, GNC, and interplanetary regimes.