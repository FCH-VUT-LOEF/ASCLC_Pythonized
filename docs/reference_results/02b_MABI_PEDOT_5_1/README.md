# 02b_MABI_PEDOT_5_1: saved numerical reference results

Source: [02b_MABI_PEDOT_5_1.xlsx](../../../data/02b_MABI_PEDOT_5_1.xlsx).
SHA-256: `0e813727698c5e1a05014d1e8cb33af6de0fc9c8e07f9d8d2a83f719e89b195b`.

These reference files exist for checking intermediate Python results against
saved source values. They are snapshots, not a recalculated or physically
validated solution. No source file or calculation parameter was changed.

| File | Source sheet | Rows |
| --- | --- | ---: |
| [measurements.csv](measurements.csv) | Data-calculations | 499 |
| [inferred_results.csv](inferred_results.csv) | MODEL | 499 |
| [dos.csv](dos.csv) | g(E) | 3001 |
| [fermi_probabilities.csv](fermi_probabilities.csv) | FD-funkce | 6001 |
| [occupations.csv](occupations.csv) | n(E) | 3001 |
| [transport.csv](transport.csv) | j(U) | 3001 |
| [controls.csv](controls.csv) | cell-addressed | 152 |
| [errors.csv](errors.csv) | cell-addressed | 15 |

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
| First processed voltage | `Data-calculations!E13` | 1.4360000000000001E-2 |
| First gamma | `Data-calculations!K13` | 0 |
| First inferred free density | `MODEL!K9` | 4.5919681062008742E+19 |
| First labelled trapped density | `MODEL!M9` | 1.7871745512329891E+20 |
| First inferred theta | `MODEL!Q9` | 0.25694010151570418 |
| Equilibrium free electron density | `n(E)!F3` | 6.6165582701311653E-7 |
| Equilibrium free hole density | `n(E)!N3` | 9.5377143252703576E+19 |
| Model gamma | `j(U)!C6` | 6.4935064935064929E-2 |
| First model hole voltage | `j(U)!C9` | 367325.88627661468 |
| First model hole current density | `j(U)!E9` | 2748294435635324 |

Verified exact CSV read-back of 157,525 mapped table cells plus all control/error records.
