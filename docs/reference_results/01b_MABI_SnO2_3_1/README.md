# 01b_MABI_SnO2_3_1: saved numerical reference results

Source: [01b_MABI_SnO2 _3_1.xlsx](../../../data/01b_MABI_SnO2%20_3_1.xlsx).
SHA-256: `6515148a5882f9766489af4ea6f5b9d6edd49fa25788b9fb287fa25faf7d6373`.

These reference files exist for checking intermediate Python results against
saved source values. They are snapshots, not a recalculated or physically
validated solution. No source file or calculation parameter was changed.

| File | Source sheet | Rows |
| --- | --- | ---: |
| [measurements.csv](measurements.csv) | Data-calculations | 500 |
| [inferred_results.csv](inferred_results.csv) | MODEL | 500 |
| [dos.csv](dos.csv) | g(E) | 3001 |
| [fermi_probabilities.csv](fermi_probabilities.csv) | FD-funkce | 6001 |
| [occupations.csv](occupations.csv) | n(E) | 3001 |
| [transport.csv](transport.csv) | j(U) | 3001 |
| [controls.csv](controls.csv) | cell-addressed | 143 |
| [errors.csv](errors.csv) | cell-addressed | 2553 |

`source_row` is the original sheet row, not a Python array index. Use
`manifest.json` for exact source-column mappings and file hashes. Formula
results are copied from the saved caches; numeric text is preserved exactly.
Errors such as `#VALUE!` remain in tables and are also listed in `errors.csv`.
Empty fields mean absent/empty saved values, not zero. Zero is preserved.
`controls.csv` stores numeric control-panel and equilibrium-reference cells
with sheet/cell addresses, including switches and all relevant temperatures.

The measurement and inferred-result tables stop at the final raw measurement;
model tables preserve the complete selected grids, including terminal error
rows. Derivative failures must not be interpreted as zero. The final DOS row
is an integration boundary; occupation sums use the preceding 3000 intervals.
Inactive DOS components are retained as components, and the switched total
is exported separately. Raw temperature values preserve source conventions;
the processed temperature column is in kelvin.

Names containing `labelled` preserve the source interpretation, not a physical
assertion about the density decomposition. Likewise the signed populations
and unbounded theta values are retained. See the [comparison](../../workbook_comparison.md)
and the [reference index](../README.md) before interpreting differences.

## Example saved values

| Quantity | Source cell | Stored value |
| --- | --- | ---: |
| First processed voltage | `Data-calculations!E13` | 4.3868999999999999E-4 |
| First gamma | `Data-calculations!K13` | 0 |
| First inferred free density | `MODEL!K9` | -1.8259988736451094E+20 |
| First labelled trapped density | `MODEL!M9` | 3.0913268455056183E+19 |
| First inferred theta | `MODEL!Q9` | -5.9068450697792461 |
| Equilibrium free electron density | `n(E)!F3` | 3.7592398954266115E-7 |
| Equilibrium free hole density | `n(E)!N3` | 1.6787030096629776E+20 |
| Model gamma | `j(U)!C6` | 1.6233766233766232E-2 |
| First model hole voltage | `j(U)!C9` | 60149.881594038474 |
| First model hole current density | `j(U)!E9` | 1185894270348.9636 |

Verified exact CSV read-back of 157,546 mapped table cells plus all control/error records.
