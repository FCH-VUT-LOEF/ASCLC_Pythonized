# Localized sources of the numerical discrepancies

Investigation date: 2026-11-01. All parameters, numerical grids, source
snapshots, notebooks, and calculation code were kept unchanged. This is a
diagnosis, not an implemented correction.

## Experimental theta: fitted slope and the transport denominator

The first processing difference is `asclc_workflow.run_effective_mobility`:
it calculates forward-window means and fits gamma over 11 points. The source
files use their stored one-point setting, which gives gamma=0. There is no
evidence that the Python CSV loader causes the discrepancy: both new inputs
match the saved raw numeric pairs exactly.

The inferred mobility contains the shape factor

    D(gamma) = (1-gamma)(2-gamma)^2
    theta = L^3 |J| / [epsilon mu0 D(gamma) U^2].

For positive source currents, compare the existing outputs algebraically:

    theta_python/theta_source
      = (|J_python|/J_source) (U_source/U_python)^2
        [4 / D(gamma_python)] (epsilon0_source/epsilon0_python).

The factor 4 is D(0), not a fitted multiplier. Geometry, relative
permittivity, and microscopic mobility are the same for each source/notebook
pair. The permittivity constant ratio is about 0.999978788; no constant was
substituted in either calculation.

At each new dataset's largest positive Python theta:

| Quantity | 01b | 02b |
| --- | ---: | ---: |
| Source Data-calculations row | 21 | 35 |
| Corresponding MODEL row | 17 | 31 |
| Saved gamma | 0 | 0 |
| Python fitted gamma | 0.9975485790 | 0.9020344306 |
| Source theta | 0.05456603191 | 0.1104759467 |
| Python theta | 53.95909319 | 3.196318669 |
| Shape-factor amplification, 4/D | 1623.736014 | 33.86952307 |
| Averaged-current factor | 1.609741821 | 1.220120336 |
| Processed-voltage-squared factor | 0.3783378850 | 0.7001318018 |
| Observed theta ratio | 988.8769863 | 28.93225868 |

The product of these factors including the permittivity ratio reproduces
the observed theta ratio. No alternate fit or smoothing experiment was run.
The near-singular denominator explains the numerical amplification in 01b;
the 02b factor is smaller but still sufficient for theta>1.

For gamma=1 the inversion diverges; for gamma>1 it changes sign. This is a
limitation of applying this transport inversion near an ohmic slope, not an
array-indexing or plotting error. This calculation alone does not establish
which contact mechanism creates the measured slope.

## Negative experimental trapped density: a different decomposition

`asclc_backend.carrier_densities`, in its default `free_over_total` branch,
sets

    p_s = p6
    p_t = p_s - p_f
    theta = p_f/p_s.

At positive p_s, theta>1 therefore necessarily makes p_t negative. At
gamma>1 and positive voltage, p6 itself is negative, so negative trapped
densities can also occur without theta>1. These identities explain why 01b
has more negative trapped rows than rows with theta>1.

The source MODEL M column is instead p6, without the subtraction, and O is
p_f+p6. Its Q column still uses the mobility ratio, p_f/p6. Thus the source
and Python trapped columns are different quantities, and the source's ratio
is not p_f/O. A direct difference between these trapped columns cannot be
treated as a same-definition accuracy measure. Both conventions need to be
judged against the physical charge definitions; neither is validated merely
because its plotted trapped density is positive.

The current model occupation definitions also mix excess and absolute
populations, as already documented in [the occupation review](../../M2_excel_conventions.md).
For the experimental curves, however, the above slope/decomposition chain
already explains the reported negative values without invoking a DOS shape.

## 01b model: localized integration error in the trap contribution

The active distribution is the same symmetric sech profile in the source
and Python. In 01b its width kB Tt/e is about 0.000431 eV. The source grid
spacing is 0.003 eV, and the trap centre -5.625 eV lies at a grid node.
The current notebook integrates at its existing 0.00075 eV spacing.

| Trap area / Nt | Value |
| --- | ---: |
| Saved source rectangle sum | 1.7478868202 |
| Current Python rectangle sum | 0.7962675383 |
| Exact full-line area of the mathematical formula, pi/4 | 0.7853981634 |

The source's peak sample alone is strongly overweighted by its interval
width. The current grid has a residual area error of about 1.38% relative
to pi/4, so the finer existing calculation is not presumed exact either.

To localize the model density discrepancy, decompose the existing total DOS
into its valence, conduction, and trap contributions. For each component:

    delta_p_component(EF)
      = sum_i dE_i g_component(E_i) [h(E_i,EF)-h(E_i,EF0)],
    h = 1-f.

This is an accounting identity for the existing excess-hole sum, not an
alternate model or a parameter change. Source occupations use their saved
Fermi lookup values and equilibrium probabilities; Python probabilities
use its existing grid and temperature. Neither grid is resampled.

Across the 53 matching EF rows where both hole voltages fall within the
measured range, the median trap share of the excess-hole-density residual
is **0.999984575**, or **99.99846%**. Its range is about 99.8149% to
100.0006%; a share above 100% means another component partially cancels it.
The largest closure residual between the component accounting and the
cached-total difference is 1.36e13 m^-3, tiny compared with the approximately
1e21-1e22 m^-3 residuals being explained and consistent with cancellation
of large background sums.

For example, at EF=-5.70899999999988 eV (`n(E)` row 1106):

- Python minus source excess holes: -3.533680309e22 m^-3.
- Trap contribution to that difference: -3.533625801e22 m^-3.
- Valence-band contribution: -5.450760249e17 m^-3.
- Conduction-band contribution: approximately 3.27e-43 m^-3.

The row-resolved accounting is saved in
[model_error_components.csv](01b_MABI_SnO2_3_1/model_error_components.csv).
The quadrature difference, not a missing double-exponential component,
accounts for the dominant model-density residual. At the same EF, model
voltage is proportional to its labelled charge and current multiplies that
voltage by the free population; the charge residual therefore propagates
into the large voltage/current discrepancy.

## Scope of the conclusion

There are separate sources of disagreement: slope processing and density
definitions for the experimental inversion, and trap quadrature for the
large 01b model difference. Rounded constants and band quadrature cause
smaller differences. No contact boundary law is implemented in either
calculation, so numerical agreement cannot establish injection-layer physics.
No code, parameter, grid, or source result has been changed during this audit.

## Carrier-density screenshot follow-up

The user's supplied log/log screenshot shows `pt`, `pf`, `ptm`, and `pfm`.
The source series definitions are MODEL E/M, E/K, Z/AJ, and Z/AH.
The current plot uses carriers.U/p_t, carriers.U/p_f, model_current.U_p/model.p_t,
and model_current.U_p/model.p_f respectively. In particular, the first pair
does not compare the same trapped-density definition: source M is p6,
whereas the current default experimental p_t is p6-p_f. The model labelled
trapped density retains yet another reference convention, p_s-p_f0.
The common legend notation therefore does not imply identical mathematical
quantities across the source and Python, or measured and model series.

Both supplied new files' charge-density chart caches were checked against
their saved MODEL cells (`chart4.xml` and `chart8.xml`, both measured series).
They agree exactly on every available measurement row: 500 rows for 01b
and 499 for 02b. Stale chart caches relative to those saved cells do not
explain this mismatch.

The screenshot's measured trapped curve dips and rises. That behavior
cannot be produced by the saved p6 expression with gamma=0 and fixed
geometry: under those settings p6 is exactly proportional to adjusted
voltage. Thus the screenshot is not the same calculation/display state as
the saved gamma=0 reference snapshots; it must not be treated as a numerical
reproduction target for those snapshots without identifying the state change.
This observation does not identify which setting or formula differs in
the screenshot, and no parameter values have been inferred or substituted.
