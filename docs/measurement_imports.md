# Standardized measurement inputs

Saved calculated and intermediate numerical results are available separately
under [`docs/reference_results/`](reference_results/README.md) for all three
sources. Those reference tables complement the raw two-column CSVs below;
they do not alter the measurement format or supply runtime model inputs.

On 2026-11-01 the user requested conversion of every `.xlsx` file in
`data/` to the project's standard measurement CSV format, `U(V),I(A)`.

All three sources identify raw voltage in volts and raw current in amperes
in columns A and B of `Data-calculations`, with headers on row 12.

| Source in `data/` | Source range | CSV in `data/` | Measurement rows |
| --- | --- | --- | ---: |
| `01b_MABI_SnO2 _3_1.xlsx` | `Data-calculations!A13:B512` | `01b_MABI_SnO2 _3_1.csv` | 500 |
| `02b_MABI_PEDOT_5_1.xlsx` | `Data-calculations!A13:B511` | `02b_MABI_PEDOT_5_1.csv` | 499 |
| `SCLCKopecky.xlsx` | `Data-calculations!A13:B226` | `SCLCKopecky.csv` | 214 |

The initial exports preserved the stored numeric text. At the user's
subsequent request on 2026-11-01, all three CSVs were rounded to match the
previous measurement CSV format: scientific notation with ten digits after
the decimal point and lowercase `e` (`.10e`, eleven significant digits).
The user's final formatting instruction supersedes scientific notation:
all three CSVs now use ordinary decimal notation, preserving those rounded
numeric values exactly. The subsequent instruction requires consistent
decimal places: voltage uses 13 places and current uses 23 places across
all three files, sufficient to preserve every rounded value. Trailing zeros
pad shorter values. No additional rounding is applied.
Signs, zeros, row order and all measurement pairs are preserved.
No unit conversion is needed. Empty rows after the
measurement ranges and unrelated columns are omitted. These are raw
voltage/current exports, without smoothing, voltage offsets, current-density
conversion, sorting or resampling. The selected cells contain numeric
values rather than formulas. Before formatting, each CSV was read back and
checked against every selected source pair and loaded with
`load_measurements`. After formatting, each saved field was checked against
the requested `.10e` representation of its original exported value. The
subsequent decimal formatting was verified with exact decimal arithmetic
to preserve each rounded value, with no exponent notation remaining.

The source files, notebook and existing parameter settings are unchanged.
Distribution models and their parameters are not represented by this
two-column measurement format; exporting the measurements does not configure
the corresponding model.

The user intends to use the new inputs to investigate assumptions tied to
the previous sample, including support for different distribution models.
This conversion does not establish that the current calculation supports
those models. Their equations and configuration need separate investigation
before implementation.
