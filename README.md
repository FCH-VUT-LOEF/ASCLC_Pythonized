[README.md](https://github.com/user-attachments/files/34249854/README.md)
# ASCLC_Pythonized

An early-stage Python prototype for analytical space-charge-limited current (A-SCLC) analysis. It converts measured current–voltage data into current density, local logarithmic slopes, effective mobility, labelled carrier concentrations, and quasi-Fermi-level estimates, and compares these quantities with a density-of-states occupation model.

The project is under active development. The notebooks are working examples for exploring the calculations; their organization, settings, and outputs may change. Shared modules handle numerical calculations and plotting.

## What it does

- Import voltage and current measurements from CSV.
- Plot raw and smoothed current density and estimate the local slope `gamma = d ln|U| / d ln|j|`.
- Calculate effective mobility and free and labelled trapped carrier densities.
- Construct parabolic valence/conduction bands and a localized sech trap distribution.
- Evaluate Fermi–Dirac occupations, equilibrium-referenced populations, and model transport quantities.
- Compare measured and model curves, including density derivatives and mobility.
- Optionally overlay model calculations at several temperatures.
- Export figures as PNG and SVG, together with a measured-data CSV.

This is an analysis workflow with explicitly supplied parameters. It does not automatically fit parameters or solve the spatial transport equations.

## Getting started

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/FCH-VUT-LOEF/ASCLC_Pythonized.git
cd ASCLC_Pythonized
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Or in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the notebook dependencies and start JupyterLab:

```bash
python -m pip install --upgrade pip
python -m pip install "numpy>=2.0" matplotlib jupyterlab
jupyter lab notebooks/asclc.ipynb
```

NumPy 2.0 or newer is needed by the notebook's `np.trapezoid` diagnostic. The modules are imported directly from this checkout; no package installation is required.

You can also open the notebooks in VS Code with its Python and Jupyter extensions and select the virtual environment as the notebook kernel.

## Example notebooks

The `notebooks/` directory contains examples using the included measurement datasets. They demonstrate the current calculations and plots and serve as development examples rather than a finalized user interface.

Input paths and sample parameters are set directly in each notebook. The examples can be inspected and run cell by cell in JupyterLab or VS Code.

## Measurement format and units

The input must be a comma-separated UTF-8 text file with this exact header:

```csv
U(V),I(A)
```

Each following row must contain exactly two numeric values: voltage in volts and current in amperes. A UTF-8 byte-order mark is accepted. Convert other units before importing; the CSV loader does not convert units.

Raw signs, row order, and nonfinite values are preserved. Derived quantities apply their documented validity checks; nonpositive coordinates cannot appear on logarithmic axes.

| Quantity | Unit / convention |
| --- | --- |
| Voltage | V |
| Current | A |
| Current density | A/m² |
| Device area | m² |
| Thickness | m |
| Mobility | m² V⁻¹ s⁻¹ |
| Carrier concentration | m⁻³ |
| Energy | eV, on a common reference scale |
| Density of states | m⁻³ eV⁻¹ |
| Temperature | K |
| Effective mass parameters | Multiples of the electron rest mass |

The notebook configuration separates experiment settings, material properties, model parameters, device settings, and the numerical window. Current density is `J = I / device["area"]`; the adjusted voltage is `V = U + device["voltage_offset"]`.

The local logarithmic slope is fitted using raw voltage before the configured offset. Transport formulas use the adjusted voltage. Mobility and measured carrier calculations share the same forward-looking window anchored at each row; incomplete windows remain `nan`. The centered smoothing curve is a separate plotting aid.

## Temperature sweeps and chart limits

The configuration cell contains `temperature_sweep`. Enable it and supply the desired `start`, `stop`, and `step` in kelvin, then rerun the notebook. The stop is included only if reached by a step. The sweep recalculates model quantities; measured quantities retain the configured experimental temperature.

Each chart has an `apply_limits` call. An axis end can be a number or `"auto"`. Automatic limits for measured/model comparisons follow measured data; explicit display bounds take precedence. Display limits do not change calculated arrays.

## Outputs

The final export cell writes every registered figure as PNG and SVG and creates `measured.csv` with these columns:

```text
U_V,I_A,V_V,J_Am2
```

These are the raw voltage, raw current, adjusted voltage, and current density. The general notebook writes to `outputs/`; sample notebooks use separate subdirectories. The export helper does not export every intermediate model array.

## Scientific conventions and interpretation

Read the linked notes before interpreting measured/model agreement:

- **Experimental carrier convention:** the default `theta_model="mobility_ratio"` labels the Poisson-derived expression as `p_t`, defines `p_s = p_f + p_t`, and reports `theta = p_f / p_t = mu_eff / mu_0`. This theta is not a bounded free-carrier fraction; equal labelled populations give theta = 1. See [carrier-density conventions](docs/carrier_density_convention.md).
- **Model occupations:** free populations are absolute, total populations are equilibrium-subtracted, and labelled trapped populations follow a separate subtraction convention. Model theta uses an absolute free/total ratio. These definitions differ from the experimental ratio. See [occupation definitions and provenance](docs/M2_excel_conventions.md).
- **Trap normalization:** the implemented distribution is `g_t(E) = N_t / (4 kT_t cosh((E-E_t)/kT_t))`, with `kT_t = k_B T_t / e` in eV. Its integral is `(pi/4) N_t`, so `N_t` is a concentration scale. See the [analysis guide](docs/ASCLC_guide.md).
- **Transport mapping:** model electron and hole curves are separate single-carrier constructions. The current mapping retains the established density conventions and is an algebraic continuation, with physical limitations described in [M4](docs/M4_model_current.md) and [M5](docs/M5_model_mobility.md).
- **Contacts and carrier identity:** the shared experimental inversion uses hole quantities. Its applicability to each device requires independent evidence about contacts and polarity; an injection-layer filename alone does not establish the dominant carrier. See [sample notes](docs/sample_notebooks.md).

Singularities, signed results, and ratios above one are retained where the implemented formulas produce them. Plotting gaps or agreement between curves do not establish that the assumed transport regime applies.

## Repository layout

| Path | Purpose |
| --- | --- |
| `asclc_backend.py` | CSV loading, physical constants, numerical functions, DOS and occupations |
| `asclc_workflow.py` | Notebook-facing calculations, result containers and export |
| `asclc_plotting.py` | Matplotlib figures and comparison plots |
| `notebooks/` | Working examples for development and exploration |
| `data/` | Measurement CSVs and scientific source files |
| `docs/` | Derivations, conventions, chart notes and reference comparisons |
| `test_asclc_*.py` | Numerical and workflow checks |

Scientific reference material includes the 2025 *Communications Physics* article by Gavranovic, Zmeskal, Weiter and Pospisil and its supplementary information. See [sources and equations](docs/ASCLC_guide.md#sources). Runtime calculations load measurement CSVs and use explicitly supplied parameters.

## Development checks

From the repository root, with the analysis dependencies installed:

```bash
python -m pip install pytest
python -m pytest
```

The existing tests cover CSV handling, smoothing, local slopes, analytical transport limits, density-of-states calculations, occupations, Fermi-level calculations, and temperature workflows. Source-comparison checks and archived results are documented under [reference results](docs/reference_results/README.md).

Before changing the implementation, read [AGENTS.md](AGENTS.md). Preserve supplied parameters, numerical grids, existing user edits, and documented density conventions.

