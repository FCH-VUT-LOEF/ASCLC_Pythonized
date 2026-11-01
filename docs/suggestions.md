# Suggestions for later investigation

## 01b: free-hole model agreement with measured inference

Recorded at the user's request, 2026-11-01. Unresolved; this entry does not
authorize implementation or parameter changes.

For `notebooks/asclc_01b_MABI_SnO2_3_1.ipynb`, the current model free-hole
density `p_fm` agrees substantially worse with the measured inferred `p_f`
than the source chart appears to, particularly around 0.8–1.3 V. Near 1 V,
the current model gives approximately 3.69e22 m^-3, versus the measured
inference of 1.87e21 m^-3, a factor of about 20. The model value is
interpolated on the existing calculated voltage curve; the measured interval
is at 1.0000718 V.

The source's excessive discrete trap weight explains a substantial shift
of its model curve toward higher voltages, but explaining that numerical
difference does not explain or resolve the current model's poor agreement
with measured inference. Better integration accuracy is not evidence of a
better experimental fit. The supplied source screenshot also differs from
the saved gamma-zero calculation state, limiting direct attribution of its
apparent agreement.

### Relation to empirical trap parameters

Follow-up recorded at the user's request, 2026-11-01: the parameter most
directly confounded with the quadrature error is `N_t`, currently
9e22 m^-3 for 01b. It multiplies the trap DOS linearly. The saved source
integral is 1.7478868202 N_t, compared with 0.7962675383 N_t on the current
Python grid and the analytical full-line integral pi N_t/4. Thus the saved
source assigns about 2.1951 times the current integrated trap weight at
the same N_t. This is an integrated-weight comparison, not a universal
multiplier for free density or voltage, whose values also depend on
occupations, equilibrium subtraction, and band contributions.

The narrow width parameter `T_t=5 K` gives k_B T_t/e approximately
0.000431 eV, much smaller than the source's 0.003 eV integration spacing.
The trap centre `E_t=-5.625 eV` coincides with a source grid node. Together
the width and grid alignment produce excessive weight at the sampled peak.
The current Python spacing is 0.00075 eV and its trap-area error relative
to the analytical integral is still about 1.38%.

If N_t or other trap parameters were fitted using the coarse source
quadrature, they could have compensated for that error. This is a plausible
fitting-history hypothesis, not an established fact. Investigate original
parameter provenance before drawing that conclusion. This suggestion does
not authorize rescaling N_t or changing T_t, E_t, or either numerical grid.

Suggested follow-up: derive and audit the connection between model
occupations, charge definitions, voltage mapping, and measured free-density
inference, including assumptions and boundary conditions. Determine why the
current model predicts the free-density rise too early. Keep all existing
physical parameters, smoothing settings, numerical grids, and occupation
definitions unchanged during diagnosis; do not compensate by tuning or
arbitrary scaling. Any implementation requires a separate user instruction.

Supporting numerical diagnosis:
[localized discrepancy sources](reference_results/comparison/error_sources.md)
and [carrier-density convention](carrier_density_convention.md).
