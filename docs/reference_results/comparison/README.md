# Comparison with the current Python results

**Historical comparison:** these residuals were generated before the user's
2026-11-01 switch to the [source density convention](../../carrier_density_convention.md).
They record the previous `free_over_total` default and have been retained as
diagnostic evidence. They are not results from the new default.

The follow-up [error-source investigation](error_sources.md) localizes the
experimental theta amplification and the 01b model discrepancy, with a
component-by-component numerical accounting.

Run date: 2026-11-01. The current three sample notebooks were evaluated with
their existing configuration cells, formulas, constants, and grids. No source,
measurement, parameter, notebook, or backend file was changed. Only comparison
data and documentation were written. Reference and input hashes are recorded
in [details.json](details.json). Calculation statements were read from the
notebooks; plotting and output-export statements were not executed.

## Main results

Raw measurements agree exactly for 01b and 02b; SCLCKopecky differs only by
the documented measurement CSV rounding (maximum relative difference below
4.7e-11). Importing voltage/current is not the source of the large discrepancies.

The largest experimental discrepancies arise after loading: sources store
gamma=0 from a one-point fit, whereas Python computes 11-point averages and
slopes. In addition, the source and Python assign different meanings to the
Poisson-derived density. These differences exist for all three samples.

| Dataset | Median relative difference, inferred free density | Median relative difference, labelled trapped density | Negative trapped rows: source / Python | Theta > 1 rows: source / Python |
| --- | ---: | ---: | ---: | ---: |
| [SCLCKopecky](SCLCKopecky/README.md) | 57.67% | 10.84% | 0 / 0 | 1 / 0 |
| [01b_MABI_SnO2_3_1](01b_MABI_SnO2_3_1/README.md) | 27.65% | 79.32% | 0 / 117 | 0 / 59 |
| [02b_MABI_PEDOT_5_1](02b_MABI_PEDOT_5_1/README.md) | 62.58% | 87.61% | 0 / 87 | 0 / 87 |

These percentages compare the same original row anchor; the processed
voltages differ because Python averages forward. They quantify current
pipeline disagreement, not isolated formula errors or equal-voltage fit errors.
In particular, theta has the same algebraic mobility-ratio expression in
both pipelines: its discrepancy is not caused by renaming p6 as total or
trapped density. The different decomposition changes the reported trapped
density; the averaging, slope, sign and constant conventions change theta.

Model differences are separate. At matching EF rows where both model hole
voltages fall inside the measured voltage range:

| Dataset | Pairs | Median relative difference, model free holes | Median relative difference, model labelled trapped holes | Median relative difference, model theta | Median relative difference, model hole current |
| --- | ---: | ---: | ---: | ---: | ---: |
| SCLCKopecky | 74 | 1.778% | 0.09367% | 1.699% | 1.924% |
| 01b_MABI_SnO2_3_1 | 53 | 0.05335% | 52.07% | 108.1% | 52.07% |
| 02b_MABI_PEDOT_5_1 | 11 | 0.09407% | 0.6763% | 0.5711% | 0.7884% |

These are paired by EF, not interpolated to equal voltage. All model arrays
and signed values are preserved. Whole-grid errors, zero-reference counts,
maximum absolute errors, source-error rows, and trailing invalid Python rows
are available in [summary.csv](summary.csv) and each dataset's detailed tables.

## What this establishes

1. Both new sources have **no negative labelled trapped experimental
   densities and no experimental theta above one**. The current Python
   pipeline introduces those particular results through its different
   processing and density convention. This does not prove the source's
   quantities have the physical meanings given by their labels.
2. 01b has a large model discrepancy near the measured range, consistent
   with its under-resolved narrow trap. Its saved trap area is 1.747887 Nt;
   the current Python rectangle integral is 0.796268 Nt; the continuous
   formula gives 0.785398 Nt. Even the current finer grid is not exact.
   No grid change or alternate-parameter experiment was performed.
3. 02b's model holes are much closer to the source, while its experimental
   densities differ strongly. It is therefore incorrect to attribute all
   of its strange experimental theta values to a missing DOS distribution.
4. This comparison alone cannot establish injection barriers, experimental
   carrier polarity, or the validity of applying the transport closure to
   either device. Those physical questions remain separate from source
   reproduction.

No tolerance-based acceptance or physical validation is claimed. Source
reproduction and governing-equation consistency are different checks.
See [the source audit](../../workbook_comparison.md) and
[the reference index](../README.md).
