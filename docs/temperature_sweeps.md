# Model temperature sweeps

User decision, 2026-11-01: offer a True/False option for plotting multiple
model datasets with user-selected start, stop, and step temperatures. Colour
maps from blue for cold to red for hot.

Each of the four sample notebooks has `temperature_sweep` in its input cell.
It defaults to `enabled=False`, retaining the configured single-temperature
calculation. Set `enabled=True`, choose `start`, `stop`, and `step` in kelvin,
and rerun all cells. The initial bounds both equal the existing experimental
temperature, so no new temperature interval is imposed by default.

The range is `start + i * step`, ending before it passes `stop`. The stop is
included if reached by an integer number of steps, allowing floating-point
roundoff. Descending sweeps use a negative step. Temperatures must be finite
and positive, and the nonzero step must point toward stop. A one-temperature
range is valid and uses blue. Temperature labels are in each chart's legend;
line styles distinguish quantities at the same temperature. Colours depend
on temperature, not on ascending or descending selection order.

## Calculation and fixed inputs

The sweep calls the existing model equations independently at each selected
temperature. For energy measured in eV,

\[
kT = k_B T/e,\qquad
f(E,E_F,T) = \frac{1}{1+\exp[(E-E_F)/kT]}.
\]

Electron and hole populations integrate the existing DOS against `f` and
`1-f`. The equilibrium populations are recomputed at the same temperature
and the fixed `E_F0`; the existing absolute and excess population definitions
are retained. Temperature changes these occupations, rather than shifting an
already calculated curve. In the current mapping the established relation is
`gamma = T_t / T` for each dataset. It is evaluated with the fixed trap-width
temperature `T_t`. Current, mobility, Fermi coordinates, and density derivatives
then use that dataset's populations on the original Fermi grid.

No material, device, trap, microscopic mobility, equilibrium energy, smoothing,
or numerical grid settings are changed. DOS curves remain shared because
their parameters do not depend on the selected model temperature. Measured
inversions retain `experiment["T"]`; the sweep does not imply measurements at
other temperatures. The Ohmic guide uses each model's own equilibrium hole
population; the temperature-independent Mott–Gurney guide is drawn once.

All model-bearing notebook charts support the sweep. Comparison limits come
from measured data before drawing model curves. Notebook-specific explicit
display bounds still take precedence, and linear/log scales are preserved.
The independent secondary free-population axis in the trapped-charge chart
uses model rows within the measured free-charge window, as specified in
[chart_scope.md](chart_scope.md). Signed/nonfinite model results and values
outside the view remain in their calculated arrays.
