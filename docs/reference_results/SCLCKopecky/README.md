# SCLCKopecky: saved numerical reference results

Source: [SCLCKopecky.xlsx](../../../data/SCLCKopecky.xlsx).
SHA-256: `f755b74181222c376f114eb687c92c50b9f3842902e53b312cc6f01c2589aa15`.

These reference files exist for checking intermediate Python results against
saved source values. They are snapshots, not a recalculated or physically
validated solution. No source file or calculation parameter was changed.

| File | Source sheet | Rows |
| --- | --- | ---: |
| [measurements.csv](measurements.csv) | Data-calculations | 214 |
| [inferred_results.csv](inferred_results.csv) | MODEL | 214 |
| [dos.csv](dos.csv) | g(E) | 3001 |
| [fermi_probabilities.csv](fermi_probabilities.csv) | FD-funkce | 6001 |
| [occupations.csv](occupations.csv) | n(E) | 3001 |
| [transport.csv](transport.csv) | j(U) | 3001 |
| [controls.csv](controls.csv) | cell-addressed | 122 |
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
| First processed voltage | `Data-calculations!E13` | 7.0311408691406405E-3 |
| First gamma | `Data-calculations!K13` | 0 |
| First inferred free density | `MODEL!K9` | 93635306275438.125 |
| First labelled trapped density | `MODEL!M9` | 55051667776805.609 |
| First inferred theta | `MODEL!Q9` | 1.7008623000316914 |
| Equilibrium free electron density | `n(E)!F3` | 0.49629442015723835 |
| Equilibrium free hole density | `n(E)!N3` | 1386704721143.2336 |
| Model gamma | `j(U)!C6` | 0.10033444816053512 |
| First model hole voltage | `j(U)!C9` | 717073615649.24658 |
| First model hole current density | `j(U)!E9` | 4.7114282736696018E+21 |

Verified exact CSV read-back of 142,537 mapped table cells plus all control/error records.
