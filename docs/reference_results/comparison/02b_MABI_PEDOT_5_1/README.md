# 02b_MABI_PEDOT_5_1: numerical comparison

Historical snapshot: this comparison predates the switch to the
[source carrier convention](../../../carrier_density_convention.md).
Its numerical tables preserve the previous default for diagnosis.

Calculated 2026-11-01 from the current sample notebook's configuration and
calculation statements, using the unchanged backend/workflow functions.
No plotting/export statements were run; no parameters or grids were changed.
These are fresh calculations, not potentially stale embedded notebook outputs.

Input hashes and all evaluated configuration values are recorded in
[`details.json`](../details.json). Source hashes and every reference CSV hash
were verified before comparison. Notebook hashes were checked again after it.

## Experimental analysis

Rows are paired by the original measurement anchor. This deliberately exposes
processing differences: the source row is a single point and the Python row
is an 11-point forward interval. These are not equal-voltage residuals.
Of 499 raw rows, 489 have a full Python slope window.
The final ten rows remain in the detailed CSV with Python missing-value status.

| Quantity | Finite pairs | Median relative difference | Maximum absolute difference | Sign mismatches |
| --- | ---: | ---: | ---: | ---: |
| U_raw_V | 499 | 0% | 0 | 0 |
| I_raw_A | 499 | 0% | 0 | 0 |
| U_processed_V | 489 | 2.016% | 0.0201509 | 0 |
| J_processed_Am2 | 489 | 3.457% | 54.7475 | 0 |
| gamma | 489 | undefined (zero references) | 0.93871 | 489 |
| mu_eff_m2Vs | 489 | 929.7% | 6.57284e-06 | 0 |
| free_density_m3 | 489 | 62.58% | 1.91063e+20 | 0 |
| labelled_trapped_density_m3 | 489 | 87.61% | 1.59209e+22 | 87 |
| labelled_total_density_m3 | 489 | 84.61% | 1.57424e+22 | 0 |
| theta | 489 | 929.7% | 3.08584 | 0 |
| E_F_absolute_eV | 489 | 0.07613% | 0.0223493 | 0 |
| density_derivative_m3eV | 488 | 86.74% | 4.02945e+26 | 0 |

Relative differences in gamma are undefined because the saved source gamma is
zero. A sign mismatch includes zero versus nonzero; it does not always mean
a positive-to-negative reversal. Relative error uses the source as denominator.
For Fermi energy use the absolute eV difference rather than the percentage
relative to the vacuum energy reference.

| Diagnostic | Source | Python |
| --- | ---: | ---: |
| Theta greater than one | 0 | 87 |
| Negative labelled trapped density | 0 | 87 |
| Minimum theta | 0.0126126 | 0.0243842 |
| Maximum theta | 0.30606 | 3.19632 |

Counts above cover each full output, including all available source points;
Python invalid trailing rows do not contribute. Source theta need not be
bounded or positive, even though its labelled trapped column is positive.

### Concrete paired anchors

| Source MODEL row | Source U (V) | Python interval U (V) | Source theta | Python theta | Source labelled trapped density (m⁻³) | Python trapped density (m⁻³) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 9 | 0.01436 | 0.034213636 | 0.25694 | 1.23577 | 1.78717e+20 | -2.94852e+19 |
| 258 | 1.01035 | 1.0303945 | 0.0157167 | 0.0763817 | 1.25743e+22 | 3.42981e+21 |
| 497 | 1.96652 | 1.9863936 | 0.0165453 | 0.0359361 | 2.44743e+22 | 1.32999e+22 |

## Model comparison at matched Fermi energies

All 3001 model rows have matching EF coordinates within 2e-12 eV. No
interpolation, fitting, alternate inputs, or alternate integrations were run.
The occupation sums use each calculation's existing integration grid.

| Quantity | Finite pairs | Median relative difference | Maximum relative difference | Sign mismatches |
| --- | ---: | ---: | ---: | ---: |
| n_s_m3 | 3001 | 0.0223% | 0.7051% | 0 |
| n_f_m3 | 3001 | 0.09728% | 4.111% | 0 |
| n_t_m3 | 3001 | 0.0223% | 0.7051% | 0 |
| theta_n | 3001 | 0.07057% | 4.089% | 0 |
| p_s_m3 | 3001 | 0.0223% | 0.7051% | 0 |
| p_f_m3 | 3001 | 0.09387% | 4.098% | 0 |
| p_t_m3 | 3001 | 0.0223% | 0.7332% | 0 |
| theta_p | 3001 | 0.1069% | 4.076% | 0 |
| dp_s_dEF_m3eV | 2999 | 0.02285% | 300% | 24 |
| U_n_V | 3001 | 0.03119% | 0.7141% | 0 |
| U_p_V | 3001 | 0.03119% | 0.7421% | 0 |
| J_n_Am2 | 3001 | 0.1492% | 4.154% | 0 |
| J_p_Am2 | 3001 | 0.07442% | 4.14% | 0 |
| mu_n_m2Vs | 3001 | 0.07057% | 4.089% | 0 |
| mu_p_m2Vs | 3001 | 0.1069% | 4.076% | 0 |

Whole-grid statistics include enormous off-view densities and tiny tail
populations. More relevant to the measured current range are the following
11 matched EF rows where **both** source and Python
hole voltages lie inside the raw adjusted measurement voltage range:

| Quantity | Median relative difference | Maximum relative difference |
| --- | ---: | ---: |
| p_f_m3 | 0.09407% | 0.1144% |
| p_t_m3 | 0.6763% | 0.7332% |
| theta_p | 0.5711% | 0.6075% |
| U_p_V | 0.6853% | 0.7421% |
| J_p_Am2 | 0.7884% | 0.8685% |

These are residuals at the same EF, **not** J errors evaluated at the same
applied voltage. The two models assign different voltages to those EF rows.
The small number of rows can limit interpretation, especially for 02b.

## DOS and equilibrium reference

DOS and equilibrium Fermi probabilities are compared on the subset of the
existing Python integration nodes coinciding with all 3001 source DOS nodes.
The grid and DOS are not altered. Both the source and Python have finite-grid
quadrature; the finer current grid is not assumed exact.

- Saved trap rectangle area / Nt: **0.7799525317**.
- Current Python trap rectangle area / Nt: **0.7853981632**.
- Continuous mathematical area / Nt: pi/4 = **0.7853981634**.

The full shared-node DOS/probability comparison is in `dos.csv`. Tail relative
errors can be large for negligible populations, and half of each band array
is the common DOS floor; whole-grid medians should not be interpreted as
relative accuracy in the physically populated band. Constant differences
also affect exponentials far into the tails.

| Equilibrium quantity | Source | Python | Relative difference |
| --- | ---: | ---: | ---: |
| n_s0 | 4.17136884e+27 | 4.17457982e+27 | 0.07698% |
| n_f0 | 6.61655827e-07 | 6.76954571e-07 | 2.312% |
| p_s0 | 5.92446929e+27 | 5.92312758e+27 | 0.02265% |
| p_f0 | 9.53771433e+19 | 9.54875781e+19 | 0.1158% |

`n_s0`/`p_s0` here denote the unsubtracted equilibrium total sums, not the
excess outputs (which vanish at EF0). Their large magnitude makes subtraction
near equilibrium susceptible to cancellation. Absolute residuals and source
zero cases are retained in the detailed files.

## Files and interpretation

- [measured.csv](measured.csv): raw/processed inputs and inferred results.
- [model.csv](model.csv): occupations, derivative, voltage/current and mobility.
- [dos.csv](dos.csv): matching DOS nodes and equilibrium Fermi probabilities.
- [equilibrium.csv](equilibrium.csv): equilibrium integrals before subtraction.
- [summary.csv](../summary.csv): aggregate errors for all datasets and scopes.

Detailed rows preserve the original source text, numeric Python result,
signed difference, relative error, and explicit error/missing-value statuses.
The relative-error column is abs(Python-source)/abs(source), undefined at
source zero. No error cells are silently treated as zero. No measured-fit
activation-energy comparison is supplied: the current notebooks do not
calculate that stage. The separate 6001-row probability lookup grid is not
recreated; its underlying function is checked here through equilibrium
probabilities on the existing shared energy nodes.

The actual source density convention differs from the Python convention:
source M is the Poisson expression p6 and source O=pf+p6; Python returns
ps=p6 and pt=ps-pf. Source theta=mu_eff/mu0 is therefore pf/p6, not pf/O.
Source fitting uses gamma=0; Python uses the fitted gamma. Source and Python
also differ in temperature paths, voltage used for the slope in 02b,
rounded constants, and signed versus absolute current in mobility.
See the [source mapping](../../../workbook_comparison.md).

Agreement with a saved source does not validate its physical assumptions.
The comparison makes no changes to remove negative densities or theta>1.

For `measured.csv`, `source_row` is the `Data-calculations` measurement
row; inferred source values come from `MODEL` at `source_row - 4`.
For `model.csv` it is the common `n(E)` / `j(U)` row; for `dos.csv`
it is the `g(E)` row. The coordinate column is raw measured voltage,
model EF, or DOS energy, respectively.

Both pipelines calculate experimental theta as the mobility ratio.
The density decomposition alone does not change theta; it changes the
reported trapped population. Nonzero slopes and averaging account for
large theta discrepancies, alongside smaller constant/sign differences.
