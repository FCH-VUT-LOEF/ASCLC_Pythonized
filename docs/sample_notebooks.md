# Sample notebooks

User decision, 2026-11-01: the general notebook `notebooks/asclc.ipynb`
uses `data/SCLCKopecky.csv` and the existing Kopecky sample configuration
from `notebooks/asclc_SCLCKopecky.ipynb`. This supersedes its previous
light-series configuration and the historical statement below that its
configuration remains untouched. Its own display bounds and general
`outputs/` export destination are preserved. Stored outputs were cleared
to prevent results from the previous sample being displayed as current.

Follow-up correction, 2026-11-01: the shared slope workflow now fits raw
voltage before its configured addition, while retaining adjusted voltage
in transport formulas. This corrects the known 02b input-path mismatch;
the later historical notes about using adjusted voltage for both paths
are superseded. Existing input values and grids are unchanged.

Current decision, 2026-11-01: experimental carriers use the
[`mobility_ratio` convention](carrier_density_convention.md): p_t is the
Poisson expression, p_s=p_f+p_t, theta=p_f/p_t. The physical alternative is
deferred. The original comparison snapshots below predate this change and
must not be mistaken for results from the new default.

Saved numerical source results for checking these notebooks now exist in
[`docs/reference_results/`](reference_results/README.md), with separate
snapshots for all three datasets. The tables are reference evidence only;
the notebooks do not load them. Consult the documented window, grid,
temperature, and density-definition differences before interpreting a
numerical mismatch.

User requirement, 2026-11-01: create three notebooks whose contents are
identical except for input paths and parameters. Maintain this invariant
when editing these notebooks: common calculations, descriptions, plotting,
metadata, and cell structure must remain identical.

User clarification, 2026-11-01: the new devices have different injection
layers. Their contact physics and selected carrier branch must therefore
be checked explicitly; a common calculation structure does not establish
that both measurements are hole-injection measurements. The filenames
identify SnO2 for 01b and PEDOT for 02b. Complete layer stacks, the precise
PEDOT formulation, and scan electrode polarity have not yet been supplied.
The current shared experimental inversion is expressed in hole quantities
and uses the valence-band DOS. Treat its applicability to 01b as unresolved,
not as a confirmed electron-only or hole-only interpretation. No carrier
branch, band reference, or contact parameter has been changed.

Follow-up source audit, 2026-11-01: both new sources explicitly select hole
labels in `MODEL!K8` and `M8`. Their conditional compares the distances
`B24 = abs(EF0-Ev)` and `B23 = abs(EF0-Ec)`; the configured distances are
0.270 versus 1.900 eV in 01b and 0.285 versus 1.885 eV in 02b. In both,
`MODEL!S9` uses Nv (`B18`) and Ev (`B14`) for the measured inversion.
The main current comparison series use `MODEL!Z` for hole voltage and
`AC` for hole current; the mobility and theta comparisons likewise use
`AF` and `AN`, the hole branches. This establishes the sources' intended
analysis convention, not the experimentally dominant carrier species.

The audit covered the sources' shared text, chart references, and text
records of embedded EMF equation images. No full device stack, labelled
electrode polarity, contact work function, or explicit contact injection
boundary law was identified. The supplied scientific article concerns
different carbon-contact devices and does not establish these new stacks.
Do not infer a complete structure or switch the source convention merely
from SnO2/PEDOT in a filename.

With the supplied mobility and other inputs held fixed, the experimental
theta expression is independent of DOS shape, band edge, effective mass,
and electron/hole naming. Thus selecting a different carrier name alone
cannot remove its values above one. Contact limitations, equilibrium
backgrounds, and validity of the assumed spatial field profile must be
distinguished from the occupation model. These are unresolved physical
interpretations, not authorization to add or alter parameters.

| Notebook | Measurement input |
| --- | --- |
| `notebooks/asclc_SCLCKopecky.ipynb` | `data/SCLCKopecky.csv` |
| `notebooks/asclc_01b_MABI_SnO2_3_1.ipynb` | `data/01b_MABI_SnO2 _3_1.csv` |
| `notebooks/asclc_02b_MABI_PEDOT_5_1.ipynb` | `data/02b_MABI_PEDOT_5_1.csv` |

The configuration is in code cell 3 (zero-based notebook cell index).
It contains the measurement path, output directory, experiment, material,
trap parameters, device voltage addition, and numerical window. Only this
cell differs across the three files. Export destinations are separate
subdirectories under `outputs/`, one per dataset.

Device and active trap values come from the corresponding source inputs
listed in [the source comparison](workbook_comparison.md), primarily
`MODEL!B8:B30`. This new notebook request is taken as authorization to
populate these new sample configurations; the original `asclc.ipynb` and
all existing backend code and parameter assignments remain untouched.
The 01b material label retains the source's Cs3Bi2I9 text despite its
MABI filename. The 02b configuration includes the source's 0.01 V addition.

All three use the current Python analysis from `asclc.ipynb`. In particular:

- The numerical window remains 11 points.
- The integration grid remains 12001 points at 0.00075 eV pitch; the
  Fermi sweep remains 3001 points at 0.003 eV pitch.
- The DOS plotting and trap-integral diagnostic grids are unchanged.
- The active DOS consists of the two parabolic bands and one sech trap.
  The source files' inactive distributions are not enabled.
- The inversion uses the configured model temperature, and the local slope
  uses the adjusted voltage, as in the current Python workflow.
- Existing explicit display bounds remain common across the copies.
  Automatic comparison bounds are still supplied by the shared plotting
  functions from measured data.

These notebooks therefore apply one existing Python workflow to three
sample configurations. They do not reproduce every source convention:
the sources' degenerate one-point fits, coarser integration grid, measured
temperature path, and raw-voltage fit path are not introduced here. The
scientific and numerical differences remain documented in the comparison.

Shared explanatory text has been generalized where the original described
one sample's noise floor or configuration. The no-crossing diagnostic no
longer infers that theta stays below one half merely because no crossing
was detected. These common edits do not change the calculated arrays.

The notebooks are delivered with cleared outputs and execution counts,
so saved results from a different sample cannot be mistaken for current
results. Validation executes all calculation and plotting cells and draws
all 16 registered figures for each sample. Export is not run during review
to avoid generating output datasets and figures in the project directory.
