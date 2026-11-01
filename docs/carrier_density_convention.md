# Experimental carrier-density convention

Follow-up correction, 2026-11-01: slope fitting now uses raw measurement
voltage before the configured addition, matching `Data-calculations!I` and
`K`. Averaged transport voltage still includes that addition, matching E.
The addition and window values themselves were not changed. The earlier
description of unchanged offset paths below records the initial convention
switch before this data-flow correction.

User decision, 2026-11-01: use the way the supplied workbooks report carrier
densities and theta. Keep the proposed physical-definition changes as a
suggestion for later. This supersedes the previous experimental default;
historical numerical comparisons retain their original results.

## Active calculation

Write epsilon = epsilon0 epsilon_r and g = gamma. At each existing processed
voltage/current interval:

    p_f = L |J| / [e mu0 (2-g) |U|]
    p_t = epsilon (1-g)(2-g) |U| / (e L^2)
    p_s = p_f + p_t
    theta = p_f / p_t = mu_eff / mu0.

The backend and workflow now default to `theta_model="mobility_ratio"`.
The source mapping is MODEL K for free density, M for labelled trapped
density, O=K+M, and Q=I/B21 for theta. Equality of the two labelled populations
is now theta=1, not theta=1/2. Theta is unbounded and is not p_f/p_s.

The current Python voltage/current magnitude convention, physical constants,
11-point window, temperature and offset paths, integration grids, sample
inputs, and all model occupation/current definitions remain unchanged.
This is a density-definition change, not a claim of exact reproduction of
all saved source values. In particular, source one-point slopes and signed
noise-floor readings still differ from the existing Python processing.

The shared plotting functions and all notebook descriptions use this
convention. The three sample notebooks still differ only in the input and
parameter cell. Obsolete embedded outputs were cleared. Existing display
bounds were preserved, including their previously authorized overrides.

Theta>1 no longer forces labelled p_t negative through subtraction. Gamma
above one can still give negative p_t, and gamma=1 still makes theta singular.
Arrays retain these results without clipping or taking their absolute values.
The measured/model overlay retains each source stage's different reference
conventions; matching their labels is not physical validation.

## Deferred suggestion: physical charge definitions

This section records a proposal, not approved active behavior. Poisson's
equation constrains net charge. Under an ideal single-carrier assumption
without compensation, the Poisson-derived expression can be interpreted
as total charge and trapped density obtained by subtracting the mobile
population. The previous explicit `free_over_total` option remains available
but is not selected by default or by the sample notebooks.

Before adopting that interpretation, derive a consistent definition of
absolute versus excess free/trapped populations, equilibrium compensation,
and contact boundary conditions through measured inference, model
occupations, and model transport. Determine when p_f/p_s can be called a
fraction and how invalid inference regions should be reported. Subtraction
can be ill-conditioned near equality, and the gamma=1 singularity is not
removed by relabelling charge. Do not add clipping, tune mobility, or change
the grid to conceal inconsistent results.

Any future implementation requires a separate user instruction. Source
snapshots under `reference_results/` remain reproduction evidence, not a
derivation of the governing equations.

## Validation

All three sample notebooks' calculation and plotting cells were executed,
excluding their export cell; all 16 registered figures per sample were drawn.
The sample notebooks remain identical outside their configuration cell.
Configuration and numerical-grid source cells were preserved exactly.
Against the previous numerical snapshots, free density and theta are
unchanged, new labelled trapped density equals the previous Poisson/total
array exactly, and new total equals that array plus free density.

Negative labelled trapped rows are now 58 for 01b, zero for 02b, and zero
for SCLCKopecky. The remaining 01b negatives come from its fitted gamma
exceeding one; they were not removed. Log/log density plots were inspected
for both new datasets. No project export files were overwritten.

The 32 focused carrier, density-derivative, Fermi-level and mobility tests
pass. Full discovery encounters two missing dependencies already absent
before this change: `tests/data/m2_reference.npz` and
`data/MAPbBr3_S2_dark.csv`. They were not recreated or replaced.

## Voltage-path correction

The user's subsequent 02b images exposed a specific implementation mismatch.
`run_effective_mobility` fitted gamma using `result.V`, which already included
the 0.01 V addition, while the source logarithm is `LN(ABS(A13))`, before
the addition. The same 11-point raw-voltage fit gives gamma=0.9912358525
in the first interval, instead of the adjusted-voltage value 0.5848721040.
At the unchanged processed U=0.03421363636 V, this changes p_t from
1.250606587e20 to 1.882098795e18 m^-3, and p_f from 1.545458605e20 to
2.168020731e20 m^-3. It explains the low-bias separation in the supplied image.

Only the slope voltage input was corrected. No sample parameters, offset,
window, integration grid, model occupations, or display limits were changed.
For zero-offset inputs, the slope is unchanged. Dependent notebook outputs
were cleared so previous results are not displayed as current. The quadratic
raw-current analytical regression check verifies that a voltage addition
cannot alter the fitted raw slope, while transport voltage retains the addition.
