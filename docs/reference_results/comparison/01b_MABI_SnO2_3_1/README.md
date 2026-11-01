# 01b_MABI_SnO2_3_1: numerical comparison

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
Of 500 raw rows, 490 have a full Python slope window.
The final ten rows remain in the detailed CSV with Python missing-value status.

| Quantity | Finite pairs | Median relative difference | Maximum absolute difference | Sign mismatches |
| --- | ---: | ---: | ---: | ---: |
| U_raw_V | 500 | 0% | 0 | 0 |
| I_raw_A | 500 | 0% | 0 | 0 |
| U_processed_V | 490 | 2.038% | 0.0201655 | 0 |
| J_processed_Am2 | 490 | 7.037% | 30.7431 | 1 |
| gamma | 490 | undefined (zero references) | 1.69547 | 490 |
| mu_eff_m2Vs | 490 | 105.7% | 3.36806e-07 | 57 |
| free_density_m3 | 490 | 27.65% | 3.68553e+22 | 1 |
| labelled_trapped_density_m3 | 490 | 79.32% | 2.09358e+23 | 117 |
| labelled_total_density_m3 | 490 | 57.05% | 1.72503e+23 | 57 |
| theta | 490 | 105.7% | 112.269 | 57 |
| E_F_absolute_eV | 490 | 0.02669% | 0.0403464 | 0 |
| density_derivative_m3eV | 489 | 72.85% | 2.5727e+27 | 0 |

Relative differences in gamma are undefined because the saved source gamma is
zero. A sign mismatch includes zero versus nonzero; it does not always mean
a positive-to-negative reversal. Relative error uses the source as denominator.
For Fermi energy use the absolute eV difference rather than the percentage
relative to the vacuum energy reference.

| Diagnostic | Source | Python |
| --- | ---: | ---: |
| Theta greater than one | 0 | 59 |
| Negative labelled trapped density | 0 | 117 |
| Minimum theta | -5.90685 | -112.063 |
| Maximum theta | 0.553569 | 53.9591 |

Counts above cover each full output, including all available source points;
Python invalid trailing rows do not contribute. Source theta need not be
bounded or positive, even though its labelled trapped column is positive.

### Concrete paired anchors

| Source MODEL row | Source U (V) | Python interval U (V) | Source theta | Python theta | Source labelled trapped density (m⁻³) | Python trapped density (m⁻³) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 9 | 0.00043869 | 0.02012079 | -5.90685 | -7.62105 | 3.09133e+19 | -2.91164e+20 |
| 259 | 1.00003 | 1.0200755 | 0.0252273 | 0.0367987 | 7.04693e+22 | 6.01722e+22 |
| 498 | 1.95628 | 1.9761582 | 0.526642 | 0.887604 | 1.37854e+23 | 1.07003e+22 |

## Model comparison at matched Fermi energies

All 3001 model rows have matching EF coordinates within 2e-12 eV. No
interpolation, fitting, alternate inputs, or alternate integrations were run.
The occupation sums use each calculation's existing integration grid.

| Quantity | Finite pairs | Median relative difference | Maximum relative difference | Sign mismatches |
| --- | ---: | ---: | ---: | ---: |
| n_s_m3 | 3001 | 0.02099% | 54.34% | 0 |
| n_f_m3 | 3001 | 0.09728% | 4.111% | 0 |
| n_t_m3 | 3001 | 0.02099% | 54.34% | 0 |
| theta_n | 3001 | 0.1018% | 123.9% | 0 |
| p_s_m3 | 3001 | 0.02099% | 54.34% | 0 |
| p_f_m3 | 3001 | 0.09387% | 4.098% | 0 |
| p_t_m3 | 3001 | 0.02099% | 61.22% | 0 |
| theta_p | 3001 | 0.1339% | 123.9% | 0 |
| dp_s_dEF_m3eV | 2999 | 0.02285% | 300% | 22 |
| U_n_V | 3001 | 0.02983% | 54.34% | 0 |
| U_p_V | 3001 | 0.02983% | 61.21% | 0 |
| J_n_Am2 | 3001 | 0.1591% | 54.24% | 0 |
| J_p_Am2 | 3001 | 0.08449% | 61.17% | 0 |
| mu_n_m2Vs | 3001 | 0.1018% | 123.9% | 0 |
| mu_p_m2Vs | 3001 | 0.1339% | 123.9% | 0 |

Whole-grid statistics include enormous off-view densities and tiny tail
populations. More relevant to the measured current range are the following
53 matched EF rows where **both** source and Python
hole voltages lie inside the raw adjusted measurement voltage range:

| Quantity | Median relative difference | Maximum relative difference |
| --- | ---: | ---: |
| p_f_m3 | 0.05335% | 0.1151% |
| p_t_m3 | 52.07% | 61.22% |
| theta_p | 108.1% | 118.7% |
| U_p_V | 52.07% | 61.21% |
| J_p_Am2 | 52.07% | 61.17% |

These are residuals at the same EF, **not** J errors evaluated at the same
applied voltage. The two models assign different voltages to those EF rows.
The small number of rows can limit interpretation, especially for 02b.

## DOS and equilibrium reference

DOS and equilibrium Fermi probabilities are compared on the subset of the
existing Python integration nodes coinciding with all 3001 source DOS nodes.
The grid and DOS are not altered. Both the source and Python have finite-grid
quadrature; the finer current grid is not assumed exact.

- Saved trap rectangle area / Nt: **1.74788682**.
- Current Python trap rectangle area / Nt: **0.7962675383**.
- Continuous mathematical area / Nt: pi/4 = **0.7853981634**.

The full shared-node DOS/probability comparison is in `dos.csv`. Tail relative
errors can be large for negligible populations, and half of each band array
is the common DOS floor; whole-grid medians should not be interpreted as
relative accuracy in the physically populated band. Constant differences
also affect exponentials far into the tails.

| Equilibrium quantity | Source | Python | Relative difference |
| --- | ---: | ---: | ---: |
| n_s0 | 4.1713974e+27 | 4.17456927e+27 | 0.07604% |
| n_f0 | 3.7592399e-07 | 3.84694327e-07 | 2.333% |
| p_s0 | 5.92452004e+27 | 5.92313126e+27 | 0.02344% |
| p_f0 | 1.67870301e+20 | 1.68030487e+20 | 0.09542% |

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
