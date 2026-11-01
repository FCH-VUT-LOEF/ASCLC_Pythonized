# Comparison of 01b, 02b, and SCLCKopecky

Read-only source review, 2026-11-01. No calculation code, source files,
parameters, grids, or notebook settings were changed. Values below are the
files' stored values; they are not proposed settings. Formula inspection and
independent arithmetic on saved arrays were used, without recalculating or
editing the workbooks.

Numerical reference snapshots now exist for all three sources in
[`docs/reference_results/`](reference_results/README.md). They contain
intermediate and final cached results, control/equilibrium cells, complete
saved-error inventories, and manifests mapping each table column to its
source cells. Use these for subsequent numerical checks; they were extracted
without recalculation or modification of the source files.

The completed [numerical comparison against the current notebooks](reference_results/comparison/README.md)
records per-row residuals and stage statistics. It distinguishes experimental
processing/decomposition differences from the model integration differences.

## Sources and structure

- [01b](../data/01b_MABI_SnO2%20_3_1.xlsx)
- [02b](../data/02b_MABI_PEDOT_5_1.xlsx)
- [SCLCKopecky](../data/SCLCKopecky.xlsx)

All contain `MODEL`, `j(U)`, `n(E)`, `g(E)`, `FD-funkce`, and
`Data-calculations`. Their common dependency flow is:

1. Raw current, voltage, and temperature plus device inputs feed the
   experimental analysis in `Data-calculations` and `MODEL`.
2. Band and trap inputs feed `g(E)`.
3. DOS arrays and Fermi probabilities feed occupation sums in `n(E)`.
4. Those populations feed voltage, current density, and mobility in `j(U)`.
5. `MODEL` collects experimental and calculated columns for comparison.

`MODEL` is therefore both an input panel and a presentation sheet, not an
independent fitting algorithm. The inspected formulas evaluate the supplied
parameters; matching displayed curves alone does not establish their physics.

The CSVs contain only raw voltage and current. They omit device geometry,
temperatures, DOS switches, parameters, and all calculated columns. See
[measurement provenance](measurement_imports.md).

## Stored inputs

Except for measurement counts and material text, these values are in
`MODEL!B8:B30`; labels are in column A. Counts refer to paired numeric
measurements in `Data-calculations!A:B`, beginning at row 13.

| Quantity | SCLCKopecky | 01b | 02b |
| --- | ---: | ---: | ---: |
| Material text, `Data-calculations!C2` | MAPbBr3 | Cs3Bi2I9 | MA3Bi2I9 |
| Measurement pairs | 214 | 500 | 499 |
| Voltage addition, V | 0 | 0 | 0.01 |
| Model temperature, K | 299 | 308 | 308 |
| Thickness L, m | 6e-4 | 2e-7 | 3.65e-7 |
| Area, m² | 7.7e-6 | 4.82e-6 | 4.5e-6 |
| Relative permittivity | 25.5 | 25.5 | 15 |
| Ec, eV | -3.36 | -3.73 | -3.73 |
| Ev, eV | -5.58 | -5.9 | -5.9 |
| Hole effective mass / electron mass | 0.305 | 0.305 | 0.305 |
| Electron effective mass / electron mass | 0.32 | 0.32 | 0.32 |
| Microscopic mobility, m²/(V s) | 2.7e-3 | 3e-9 | 2.13e-6 |
| Equilibrium EF, eV | -4.84 | -5.63 | -5.615 |
| Active trap centre, eV | -4.82 | -5.625 | -5.62 |
| Active trap Nt, m⁻³ | 4.7e16 | 9e22 | 1e23 |
| Active trap Tt, K | 30 | 5 | 20 |

The 01b filename says MABI but its internal material text says Cs3Bi2I9.
This discrepancy cannot be resolved from the filename; neither identity has
been substituted for the other. In both new files the metadata voltage text
is `(-0.1, 1) V`, while the raw measurements extend to approximately 1.996 V.

## Experimental path

The common first-row formulas are:

- `Data-calculations!E13`: forward average of raw A values plus
  `MODEL!B8` through `J2`.
- `G13`: forward average of raw B values divided by area `D4`.
- `I13`: `LN(ABS(A13))`, using raw voltage before its addition.
- `J13`: `LN(ABS(B13/D4))`.
- `K13`: `LINEST` of log voltage on log current density. With a meaningful
  multipoint fit this estimates gamma = d ln|Uraw| / d ln|J|.
- `N13`: forward average of raw C values plus 273.15.

The average/fit includes rows r through r + `I1`, so its point count is
`I1 + 1`. **All three original files currently store `I1 = 0`.** Every saved
gamma on the raw measurement rows is zero: 214, 500, and 499 values,
respectively. These are degenerate one-point fit results, not a measured
logarithmic slope. The saved activation-energy fits are likewise degenerate.
The existing Python `local_gamma` requires at least two points and therefore
cannot reproduce this control setting through its present API. No window
was changed for this review. Earlier documentation of an 11-point Python
window must not be mistaken for the current source-file setting.

With epsilon = epsilon0 epsilon_r, `MODEL!I`, `K`, `M`, `O`, `Q` implement:

    mu_eff = J L³ / [epsilon (1-gamma) (2-gamma)² U²]
    p_f = J L / [e mu0 (2-gamma) U]
    p_6 = epsilon (1-gamma) (2-gamma) U / (e L²)
    column O = p_f + p_6
    column Q = mu_eff / mu0 = p_f / p_6

Here p_6 names the expression rather than assuming its physical meaning.
The sheets label it trapped density. Under the drift/Poisson power-profile
closure, it is total space-charge number density: integrating
F(x)=F_L(x/L)^(1-gamma) gives U=F_L L/(2-gamma), and Poisson at x=L gives
p_6=epsilon (1-gamma)F_L/(e L). Thus the source's sum and ratio are not a
consistent free-plus-trapped decomposition under that closure. See
[the derivation and existing density alternatives](ASCLC_guide.md).

For 02b, the voltage addition creates a further distinction: a row with raw
U=0.00436 V uses 0.01436 V in the transport formulas, but its logarithmic-fit
voltage remains 0.00436 V. Python currently computes local gamma from the
offset voltage `result.V`, so it would differ for a multipoint fit with a
nonzero addition. The stored one-point zeros conceal this distinction.

The model uses 308 K for both new sources, whereas their first measured
temperature is 25 + 273.15 = 298.15 K. `MODEL!S` uses the per-row measured
temperature for its absolute-value Boltzmann inversion; band effective DOS
uses the sheet/model temperature. A single temperature argument cannot
reproduce both conventions. SCLCKopecky also has distinct measured and model
temperatures.

## DOS path and mathematical shapes

SCLCKopecky uses valence DOS F, conduction DOS I, trap DOS M, and total Q.
The new files retain F and I but add four localized components:

| Component in new sources | Column | Switch | 01b | 02b |
| --- | --- | --- | ---: | ---: |
| Valence band | F | E3 | 1 | 1 |
| Conduction band | I | H3 | 1 | 1 |
| Labelled valence tail | M | L3 | 0 | 0 |
| Labelled monoenergetic trap | P | O3 | 1 | 1 |
| Labelled conduction tail | S | R3 | 0 | 0 |
| Gaussian distribution | V | U3 | 0 | 0 |

`g(E)!Z13` explicitly sums these six switched components. X and Y contain
the switched conduction and valence DOS used for free carriers. In 02b,
the Gaussian switch links to `MODEL!A34`; its centre, scale, and temperature
link to `MODEL!B35:B37` (-5.57 eV, 2e19 m⁻³, 30 K). They are inactive.
01b's corresponding Gaussian values are hardcoded on `g(E)` and inactive.

Despite their different labels, M, P, and S all use the same symmetric
exponential-ratio function, each with its own centre, width, and amplitude.
They are neither one-sided exponential tails nor delta functions. Write
a=kB Tt/e in eV and u=(E-Et)/a. The active trap in all three sources is

    g_t(E) = Nt/(2a) exp(-|u|)/(1+exp(-2|u|))
           = Nt/[4a cosh(u)].

Its full continuous integral is pi Nt/4 because the integral of sech(u)
over the real line is pi. This is the implemented mathematical shape,
independently of the sheet's distribution label. It is already the shape
implemented by Python `trap_dos`.

The Gaussian uses

    g_G(E) = NG/[sigma sqrt(2 pi)] exp(-(E-EG)²/(2 sigma²)),
    sigma = kB TG/e.

Its continuous full-line area is NG. The present backend has no Gaussian
component or general list of independently switched localized components.
The active three-component cases can use the existing mathematical DOS
functions, but the present high-level workflow does not expose the extended
switch structure.

## Fixed-grid consequences

All three sources have a descending energy grid from 0 to -9 eV, with
0.003 eV spacing and 3001 points. Occupations use 3000 rectangles; the final
point is an interval boundary. Independent sums of saved width × active
trap DOS give:

| Source | Discrete trap area / Nt | Continuous area / Nt |
| --- | ---: | ---: |
| SCLCKopecky | 0.7850791 | 0.7853982 |
| 01b | 1.7478868 | 0.7853982 |
| 02b | 0.7799525 | 0.7853982 |

For 01b, a is about 0.000431 eV, narrower than one grid step, and Et=-5.625
eV lies on a grid node. The sampled peak alone contributes strongly to the
rectangular sum. Its discrete trap area is about 2.23 times the continuous
area of the same formula with the same inputs. This is a quadrature issue,
not evidence of a different trap population. Exact source reproduction
must preserve the source's grid and sum; scientific validation must report
the discrepancy. No resampling, normalization, or parameter changes were
performed or authorized.

## Occupations and transport prediction

All three use the same occupation convention, with column relocation in
the extended sources. For total DOS G and Fermi electron probability f:

    A_n(EF) = sum dE G f;       A_p(EF) = sum dE G (1-f)
    n_s = A_n(EF)-A_n(EF0);    p_s = A_p(EF)-A_p(EF0)
    n_f = sum dE g_c f;        p_f = sum dE g_v (1-f)
    n_t = n_s-n_f(EF0);        p_t = p_s-p_f(EF0)
    theta_n = abs(n_f/n_s);    theta_p = abs(p_f/p_s).

These are excess totals combined with absolute free populations. The
labelled trapped terms subtract equilibrium free populations, not the free
populations at the current EF. They therefore do not give a conventional
free/trapped partition. Theta can exceed one and becomes singular at the
equilibrium reference. These conventions are already represented in
`model_occupations`; see [the detailed occupation review](M2_excel_conventions.md).

`j(U)!C6` supplies gamma_model = Tt/T, independently of measured gamma:
0.10033445 for SCLCKopecky, 0.01623377 for 01b, and 0.06493506 for 02b.
For each carrier branch, `j(U)!B:E` computes

    U = e L² q / [epsilon (1-gamma_model)(2-gamma_model)]
    J = e mu0 f (2-gamma_model) U/L,

using the labelled trapped population for q and absolute free population
for f. Drift and Poisson require total space charge in q; the sheet's
occupation convention does not generally supply it. The implementation
can reproduce these formulas without claiming a self-consistent spatial
solution. See [transport derivation](M4_model_current.md).

## Existing errors and translation priorities

The saved files contain calculation errors. 01b has 2542 error cells on
`MODEL`, beginning with `P508`; many are in extended experimental formulas
past the available measurements. 02b and SCLCKopecky each have four
`MODEL` errors at the last two derivative rows. All three have eight
`n(E)` errors at rows 3008-3009 and three `Data-calculations` errors at row
652. These should be distinguished from valid measurement rows and valid
occupation outputs rather than blindly imported as target values.

For a subsequent authorized implementation:

1. Keep the mathematical core independent of source-file columns. Map
   source conventions and sample inputs separately; do not automatically
   replace current notebook parameters.
2. Preserve distinct raw voltage, transport voltage, measured temperature,
   and model temperature paths.
3. Make the one-point fit behavior explicit if exact saved-source
   reproduction is required; it is presently unsupported by `local_gamma`.
4. Support a sum of independently specified DOS components when the inactive
   distributions are needed. The active new-source trap does not need a new
   mathematical shape.
5. Preserve the fixed grids, rectangle sums, reference subtractions, signs,
   and supplied model gamma when comparing source outputs.
6. Validate source agreement separately from physical identities, including
   the trap integral and total-charge definition. Do not tune inputs or
   silently change conventions to resolve discrepancies.

This review identifies the mapping and gaps; it does not implement these
changes or resolve the scientific convention choices.
