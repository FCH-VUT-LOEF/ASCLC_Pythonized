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

## Running an example in VS Code — first-time setup

A notebook (`.ipynb`) combines explanatory text with small blocks of Python code called **cells**. You run the cells inside VS Code, and the results and plots appear below them. The **kernel** is the Python process that runs those cells.

### 1. Install Python and VS Code

- Install the desktop version of [Visual Studio Code](https://code.visualstudio.com/).
- Install [Python](https://www.python.org/downloads/). Python 3.12 is a suitable starting point.
- On Linux Mint/Ubuntu, Python may already be installed. Install virtual-environment support from a system terminal if needed:

```bash
sudo apt install python3 python3-venv
```

Open VS Code. Click the **Extensions** icon in the left sidebar (four squares), search for each of the following, and install the versions published by **Microsoft**:

- **Python**
- **Jupyter**

### 2. Download and open the project

1. Open [the repository](https://github.com/FCH-VUT-LOEF/ASCLC_Pythonized) in your browser.
2. Click the green **Code** button, then **Download ZIP**.
3. Extract the ZIP into a normal folder on your computer. Do not open files from inside the ZIP.
4. In VS Code, select **File → Open Folder** and open the extracted project folder.
5. In the left-hand file list, you should see `asclc_backend.py`, `asclc_workflow.py`, `notebooks`, and `data`. If you only see another folder with the project name, open that inner folder instead.

Git is optional for this route. Keep the whole folder together: the example notebooks need the Python modules and data beside them.

### 3. Create a Python environment for the project

An environment keeps this project's Python packages together.

1. Open **View → Command Palette**.
2. Type **Python: Create Environment** and select it.
3. Select **Venv**.
4. Choose your installed Python interpreter, for example Python 3.12.
5. If asked to choose a dependency file, skip that step; install the packages below.

VS Code creates a folder called `.venv` inside the project.

### 4. Install the required packages

Open **Terminal → New Terminal** in VS Code. The terminal is the text panel where you enter commands.

Use the command for your operating system, one line at a time, pressing **Enter** after each line. These commands explicitly use the project's environment, so activation is not required.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install "numpy>=2.0" matplotlib ipykernel
```

**Linux or macOS:**

```bash
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install "numpy>=2.0" matplotlib ipykernel
```

Wait until installation finishes and the terminal prompt returns. NumPy handles numerical arrays, Matplotlib draws the plots, and IPyKernel runs Python notebook cells. The example uses `np.trapezoid`, which requires NumPy 2.0 or newer.

### 5. Open the example and select its kernel

1. Expand `notebooks` in the left-hand file list.
2. Open `asclc.ipynb`. This is a working example using an included dataset.
3. Click **Select Kernel** in the notebook's upper-right corner.
4. If needed, choose **Select Another Kernel → Python Environments**.
5. Select the Python environment whose path contains this project's `.venv` folder.

Selecting the notebook kernel matters even if you already selected a Python interpreter elsewhere in VS Code. No remote Jupyter server or browser-based JupyterLab session is needed.

### 6. Run the example

For the first run, leave the example's sample parameters unchanged.

Click **Run All** in the notebook toolbar. Alternatively, select the first code cell and press **Shift+Enter** repeatedly to run cells in order.

A cell shows `[*]` while it is running and a number such as `[1]` when it finishes. Wait for the calculations to finish; plots and printed results appear below the cells. If a cell reports an error, resolve it before continuing with later cells.

The final export cell saves figures and `measured.csv` into the project's `outputs` folder. Press **Ctrl+S** to save the notebook itself.

### 7. Reopen it later

Open the same project folder in VS Code, open the notebook, check that its kernel still points to `.venv`, and click **Run All**. You do not need to recreate the environment or reinstall packages each time.

After editing inputs, rerun the notebook from the top. Use **Restart Kernel**, then **Run All**, when you want to clear variables left over from an earlier run.

### Common setup problems

| Problem | What to check |
| --- | --- |
| No Python interpreter is offered | Install Python, restart VS Code, then repeat **Python: Create Environment**. |
| Creating the environment fails on Linux Mint/Ubuntu | Install `python3-venv`, then retry. |
| No notebook controls appear | Check that Microsoft's **Jupyter** extension is installed and enabled. |
| `No module named numpy`, `matplotlib`, or `ipykernel` | Run the installation commands above and select the matching `.venv` notebook kernel. |
| `No module named asclc_workflow` or `asclc_backend` | Open the complete project folder, with the modules at its root, and keep the notebook inside `notebooks/`. |
| `FileNotFoundError` | Check that the ZIP was fully extracted and the `data/` folder and configured input file exist. |
| NumPy has no attribute `trapezoid` | Install `"numpy>=2.0"` in `.venv`, then restart the notebook kernel. |
| PowerShell says script execution is disabled | Use the explicit `python.exe` commands above; they do not require running an activation script. |

VS Code's official guides cover [notebook controls](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) and [kernel selection](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management).


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
