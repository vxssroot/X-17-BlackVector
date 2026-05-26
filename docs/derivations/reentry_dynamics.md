# Reentry Dynamics & Heating Derivations

## 3-DOF Ballistic Equations (non-rotating spherical Earth)
\[
\frac{dh}{dt} = v \sin\gamma
\]
\[
\frac{dv}{dt} = - \frac{1}{2} \rho v^2 C_d \frac{A}{m} - g(h) \sin\gamma
\]
\[
\frac{d\gamma}{dt} = \left( \frac{v}{r} - \frac{g(h)}{v} \right) \cos\gamma
\]

where \( r = R_E + h \), \( g(h) = g_0 (R_E / r)^2 \)

## Convective Heating (Sutton-Graves)
Empirical correlation for stagnation point:
\[
\dot{q}_{conv} = 1.83 \times 10^{-4} \sqrt{\frac{\rho}{R_n}} V^{3.15} \quad [\text{W/m}^2]
\]

Used directly in `ReentryModel.convective_heat_rate`.

## Assumptions & Limitations (Phase 1)
- No lift (ballistic only)
- No Earth rotation / Coriolis
- Constant Cd (extendable via Mach table)
- No thermal protection system ablation model
- Future: 6-DOF + heat shield response + breakup criteria

These equations are integrated with DOP853 in `ReentryModel.simulate_ballistic`.