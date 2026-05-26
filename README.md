# X-17 BlackVector

**Advanced Computational Aerospace Engineering Platform**

Production-grade simulation, optimization, and mission planning for rocket systems, orbital mechanics, GNC, and reentry dynamics. Integrates high-fidelity physics models with modern software engineering practices and future AI-assisted design.

## Vision
A research and engineering toolkit that bridges computational physics, systems engineering, and AI for next-generation aerospace vehicles.

## Features (Phase 1 Delivered)
- Two-body orbital propagation with Keplerian elements
- US Standard Atmosphere 1976 density & Mach model
- Tsiolkovsky propulsion + time-dependent thrust/mass
- 3-DOF ballistic reentry with Sutton-Graves heating
- Modular high-order SimulationEngine (DOP853)
- Typed Pydantic vehicle/mission configs
- Production CLI (`blackvector-sim reentry|orbit`)
- Unit tests with energy conservation checks
- Full enterprise structure, CI, and documentation

## Tech Stack
- **Core**: Python 3.11+ with NumPy, SciPy, Pandas
- **Performance**: Planned Rust core via PyO3/Maturin
- **API**: FastAPI
- **Data**: PostgreSQL for mission archives
- **Optimization**: SciPy, PuLP, future reinforcement learning / gradient-based
- **Visualization**: Matplotlib, Plotly, VTK for 3D
- **CI/CD**: GitHub Actions

## Quick Start

```bash
git clone https://github.com/vxssroot/X-17-BlackVector.git
cd X-17-BlackVector
pip install -e ".[dev]"
blackvector-sim --help
blackvector-sim reentry --alt 120000 --vel 7800 --gamma -0.4
```

Run tests:
```bash
pytest
```

See `docs/` for architecture, derivations, and roadmap.

## Project Structure (Implemented)

```
src/blackvector/
├── core/
│   ├── constants.py
│   ├── physics/          # orbital, atmosphere, propulsion, reentry
│   └── simulation/       # engine
├── models/               # pydantic VehicleConfig, MissionConfig
├── cli.py
docs/
├── architecture.md
├── roadmap.md
└── derivations/
simulations/examples/
tests/unit/
.github/workflows/ci.yml
```

## Contributing
Professional contributions welcome. Follow enterprise-grade standards.

## License
MIT (or choose appropriate for aerospace IP)

---
*Built as a founder-grade deep tech project.*