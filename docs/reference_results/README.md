# Saved numerical reference results

The references have now been [compared with the current Python results](comparison/README.md).
Detailed residual tables and per-stage statistics exist for all three datasets;
the comparison retained the current parameters and numerical settings.

Created at the user's request on 2026-11-01. Reference snapshots now exist for
all three supplied calculation sources:

- [SCLCKopecky](SCLCKopecky/README.md): 214 measurements, 142,537 checked table cells, 15 saved error cells.
- [01b_MABI_SnO2_3_1](01b_MABI_SnO2_3_1/README.md): 500 measurements, 157,546 checked table cells, 2553 saved error cells.
- [02b_MABI_PEDOT_5_1](02b_MABI_PEDOT_5_1/README.md): 499 measurements, 157,525 checked table cells, 15 saved error cells.

Each directory contains six numerical stage tables, a scalar control/reference
table, a complete saved-error inventory, a manifest with source ranges and
SHA-256 hashes, and documentation with example intermediate values.

The stages are measurements and processing, inferred experimental results,
DOS, Fermi probabilities, model occupations, and model voltage/current/mobility.
The files preserve stored numeric text without float conversion or rounding.
The originals were read as ZIP/XML only and were not recalculated or saved.
Every exported table field was read back and checked against its source value.
In total, 457,608 mapped table cells were checked, plus the control/error
records. A second read-only reader independently verified 594 fields across
the first, middle, and final rows of all six stages in all three sources.
All source hashes, exported CSV hashes, and row counts also passed verification.

## Using these references

- Pair values by `source_row`, sheet mapping, and physical coordinate, not
  simply by a CSV row number. Model coordinate grids and measurement rows
  belong to separate stages.
- For error analysis convert numeric fields deliberately; keep error and
  missing-value status visible. `errors.csv` includes errors outside the
  selected tables as well as those within them.
- Use `controls.csv` to identify the source inputs for a comparison. These
  files do not authorize changing current calculation inputs or settings.
- Source experimental fits store a one-point window and gamma=0; current
  notebooks use 11 points. Their processed rows are not identical intervals.
- Source DOS integration uses a 0.003 eV grid; current notebooks retain a
  0.00075 eV grid. Narrow-trap quadrature, especially 01b, can differ strongly.
- Rounded physical constants, separate measured/model temperature paths,
  voltage additions, and density definitions can also cause differences.
- Equilibrium subtraction of large background populations makes relative
  errors near zero misleading. Check absolute differences as well.
- Source agreement is a reproduction check, not proof of physical validity.
  No Python comparison or tolerance-based acceptance is claimed by extraction.
- Runtime calculations must continue to use mathematical inputs and measured
  data, not depend on these source snapshots.

See [source comparison](../workbook_comparison.md),
[sample notebook conventions](../sample_notebooks.md), and
[measurement provenance](../measurement_imports.md).
