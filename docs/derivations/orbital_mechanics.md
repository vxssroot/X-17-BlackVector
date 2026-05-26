# Orbital Mechanics Derivations

## Two-Body Equation of Motion
From Newton's law of gravitation:
\[
\ddot{\mathbf{r}} = -\frac{\mu}{r^3} \mathbf{r}
\]

## Vis-Viva Equation
Specific mechanical energy \(\mathcal{E} = \frac{v^2}{2} - \frac{\mu}{r} = -\frac{\mu}{2a}\)
Rearranged:
\[
v = \sqrt{\mu \left( \frac{2}{r} - \frac{1}{a} \right)}
\]

## Keplerian Elements from State
Specific angular momentum \(\mathbf{h} = \mathbf{r} \times \mathbf{v}\)

Eccentricity vector \(\mathbf{e} = \frac{1}{\mu} (\mathbf{v} \times \mathbf{h} - \mu \frac{\mathbf{r}}{r})\)

Semi-major axis from energy or \(a = \frac{h^2}{\mu(1-e^2)}\) (ellipse)

Inclination \(i = \arccos(\frac{h_z}{|\mathbf{h}|})\)

 etc. (full classical element set implemented in `TwoBodyPropagator.state_to_elements`)

## Numerical Integration
High-order explicit Runge-Kutta (DOP853) chosen for accuracy in long-duration orbital arcs with adaptive step control. Energy drift monitored in tests.