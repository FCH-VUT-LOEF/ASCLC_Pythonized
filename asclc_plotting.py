"""Matplotlib figure for measured A-SCLC results.

Formatting is plain and publication-style (default colour cycle, light grid,
power-of-ten tick labels on logarithmic axes, frameless legends). Axis titles
and series names use the notation of the published equations: Voltage, U (V) /
Current density, j (A/m2); series "j". Each function takes the ``Calculation``
returned by ``run_calculation`` and returns ``(figure, axes)``.

Model plots accept ``temperature_models`` from ``run_temperature_models``.
None retains the single-model view. A supplied sequence replaces model curves
with temperature-labelled curves, coloured from blue (cold) to red (hot).
"""
import matplotlib.pyplot as plt
from types import SimpleNamespace

from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.ticker import LogFormatterSciNotation
from matplotlib.transforms import Bbox
import numpy as np

from asclc_backend import (centered_mean, equal_density_voltage, E_CHARGE, EPSILON_0,
                           valence_band_dos, conduction_band_dos,
                           trap_dos, DOS_FLOOR, K_B,
                           fermi_dirac_probabilities)

_FIGSIZE = (7.2, 4.5)

_U_AXIS = "Voltage, $U$ (V)"
_J_AXIS = "Current density, $j$ (A/m$^2$)"
_P_AXIS = r"Carrier concentration (m$^{-3}$)"
_THETA_AXIS = r"Carrier ratio, $\Theta$ (-)"
_E_AXIS = r"Energy, $E$ (eV)"
_G_AXIS = r"Density of states, $g(E)$ (m$^{-3}$eV$^{-1}$)"

# Dimensionless visualisation aids: multiply the Ohmic amplitude by 2 and
# divide the Mott-Gurney amplitude by 0.4. These vertical shifts preserve
# logarithmic slopes of 1 and 2; they do not modify the model calculation.
_OHMIC_FACTOR = 2.0
_MOTT_GURNEY_FACTOR = 0.4


def _temperature_series(temperature_models, **baseline):
    """Share temperature colours across charts; None preserves single-model style."""
    if temperature_models is None:
        yield SimpleNamespace(**baseline), {}, ''
        return
    if not temperature_models:
        raise ValueError('Supply at least one temperature model.')
    temperatures = np.array([item.temperature for item in temperature_models])
    if not np.isfinite(temperatures).all() or np.any(temperatures <= 0):
        raise ValueError('Model temperatures must be finite and positive (K).')
    norm = Normalize(temperatures.min(), temperatures.max())
    colours = LinearSegmentedColormap.from_list('temperature', ['blue', 'red'])
    for item in temperature_models:
        yield item, dict(color=colours(norm(item.temperature))), f', {item.temperature:g} K'


def _style(ax, *, xlabel, ylabel):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="major", alpha=0.3)
    for name in ("x", "y"):
        if getattr(ax, f"get_{name}scale")() == "log":
            getattr(ax, f"{name}axis").set_major_formatter(LogFormatterSciNotation())
    ax.legend(frameon=False)
    ax.figure.tight_layout()


def _finite_positive(*arrays):
    """Boolean mask where every array is finite and strictly positive."""
    mask = None
    for values in arrays:
        values = np.asarray(values, dtype=float)
        ok = np.isfinite(values) & (values > 0)
        mask = ok if mask is None else mask & ok
    return mask


def plot_measured_jv(result):
    """Measured current density against voltage on logarithmic axes.

    Nonpositive readings are kept in the data but cannot appear on a
    logarithmic axis.
    """
    v, j = np.asarray(result.V, float), np.asarray(result.J, float)
    ok = _finite_positive(v, j)
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.plot(v[ok], j[ok], "o", ms=4, label="j")
    _style(ax, xlabel=_U_AXIS, ylabel=_J_AXIS)
    return fig, ax


def plot_smoothed_jv(result, *, window):
    """Measured current density, smoothed against unsmoothed on the same axes.

    ``window`` is ``numerics["window"]``. A centred ``window``-point mean of
    ``J`` (`asclc_backend.centered_mean`) is drawn over the raw markers at the
    same voltages, so the two can be compared directly. The points at each end
    without a full window, and nonpositive readings, do not appear.
    """
    v, j = np.asarray(result.V, float), np.asarray(result.J, float)
    j_s = centered_mean(j, window=window)
    raw, smooth = _finite_positive(v, j), _finite_positive(v, j_s)
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.plot(v[raw], j[raw], "o", ms=4, alpha=0.35, label="j")
    ax.plot(v[smooth], j_s[smooth], "-", lw=1.6,
            label=f"j, {window}-point mean")
    _style(ax, xlabel=_U_AXIS, ylabel=_J_AXIS)
    return fig, ax


def plot_effective_mobility(result, mobility, *, mu_0=None,
                            model_mobility=None, model_current=None,
                            temperature_models=None):
    """Measured and optional model hole mobility versus voltage, linear/log.

    ``mobility`` is the ``Mobility`` returned by ``run_effective_mobility``;
    the voltage is its trailing-mean ``U``, the value each row describes.
    Linear voltage against logarithmic mobility, the axes of the published
    Fig. 3. ``mu_0`` (m^2 V^-1 s^-1), if given, is a dashed reference.
    Model mobility and voltage must share the same energy sweep. Their hole
    arrays are paired row by row without resampling. Both limits come from
    measured points before adding the model or reference line.
    Points with no value (the ends without a full window, ``U = 0``, a
    vanishing shape factor) and points where Eq. (4) returns a negative mobility
    (``gamma > 1``) are kept in the data but cannot appear on a logarithmic
    axis.
    """
    if (model_mobility is None) != (model_current is None):
        raise ValueError('Supply both model mobility and model current.')
    if model_mobility is not None:
        if not np.array_equal(model_mobility.E_F, model_current.E_F):
            raise ValueError('Model mobilities and voltages must share the E_F sweep.')
        if any(np.shape(a) != np.shape(model_mobility.E_F)
               for a in (model_mobility.mu_p, model_current.U_p)):
            raise ValueError('Model hole mobility and voltage must match the E_F sweep.')
    v, mu = np.asarray(mobility.U, float), np.asarray(mobility.mu_eff, float)
    ok = np.isfinite(v) & _finite_positive(mu)
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_yscale("log")
    ax.plot(v[ok], mu[ok], "o", ms=4, label=r"$\mu_d$")
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    for dataset, colour, suffix in _temperature_series(
            temperature_models, model_mobility=model_mobility, model_current=model_current):
        model_mobility, model_current = dataset.model_mobility, dataset.model_current
        if model_mobility is None:
            continue
        if not np.array_equal(model_mobility.E_F, model_current.E_F):
            raise ValueError("Model mobilities and voltages must share the E_F sweep.")
        valid = np.isfinite(model_current.U_p) & _finite_positive(model_mobility.mu_p)
        ax.plot(np.where(valid, model_current.U_p, np.nan),
                np.where(valid, model_mobility.mu_p, np.nan),
                label=r'$\mu_{d,m}$ (p)' + suffix, **colour)
    if mu_0 is not None:
        ax.axhline(mu_0, ls="--", lw=1.2, color="0.35", label=r"$\mu_0$")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    _style(ax, xlabel=_U_AXIS,
           ylabel=r'Drift mobility, $\mu$ (m$^2$/V/s)')
    return fig, ax


def plot_local_gamma(result, mobility):
    """Local slope parameter gamma against the trailing-mean voltage.

    The horizontal lines mark the reference slopes of the model: ``gamma = 1``
    (ohmic, where Eq. (4) diverges) and ``gamma = 1/2`` (Mott-Gurney).
    """
    v, g = np.asarray(mobility.U, float), np.asarray(mobility.gamma, float)
    ok = _finite_positive(v) & np.isfinite(g)
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_ylim(-0.2, 1.6)
    for level, name in ((1.0, "ohmic"), (0.5, "Mott-Gurney")):
        ax.axhline(level, ls="--", lw=1.0, color="0.5")
        ax.annotate(name, (0.01, level), xycoords=("axes fraction", "data"),
                    va="bottom", fontsize="small", color="0.4")
    ax.plot(v[ok], g[ok], "o", ms=4, label=r"$\gamma$")
    _style(ax, xlabel=_U_AXIS, ylabel=r"Slope parameter, $\gamma$ (-)")
    return fig, ax


def plot_carrier_densities(carriers, *, model=None, model_current=None,
                           xscale="linear", temperature_models=None):
    """Free and trapped concentrations against voltage, the axes of Fig. 4a.

    ``carriers`` is the ``Carriers`` returned by ``run_carrier_densities``:
    ``p_f`` from equation (5), ``p_t`` from equation (6) under the reading named
    by ``carriers.theta_model``. Where the two cross, the charge starts to
    occupy the transport band (guide step A4); each crossing is drawn as a
    vertical line. Linear voltage against logarithmic concentration, as in
    Fig. 4a and as in ``plot_effective_mobility``. Nonpositive values -- the
    rows where equation (6) turns negative, or an explicitly selected
    total-charge decomposition gives a negative trapped population -- stay
    in the data but cannot appear on a logarithmic axis. Supplying model
    occupations and their paired voltages
    adds both hole densities on U_p and omits crossing annotations. Display
    limits follow the measured densities only. Set ``xscale="log"`` for
    logarithmic voltage; nonpositive voltages then cannot be displayed.
    """
    if xscale not in ("linear", "log"):
        raise ValueError('Voltage scale must be linear or log.')
    if (model is None) != (model_current is None):
        raise ValueError('Supply both model occupations and model current.')
    if model is not None and not np.array_equal(model.E_F, model_current.E_F):
        raise ValueError('Model densities and voltages must share the E_F sweep.')
    v = np.asarray(carriers.U, float)
    p_f, p_t = np.asarray(carriers.p_f, float), np.asarray(carriers.p_t, float)
    voltage_valid = _finite_positive(v) if xscale == "log" else np.isfinite(v)
    free = voltage_valid & _finite_positive(p_f)
    trapped = voltage_valid & _finite_positive(p_t)
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_xscale(xscale)
    ax.set_yscale("log")
    ax.plot(v[trapped], p_t[trapped], "o", ms=4, label=r"$p_t$ (m$^{-3}$)")
    ax.plot(v[free], p_f[free], "o", ms=4, label=r"$p_f$ (m$^{-3}$)")
    has_model = model is not None or temperature_models is not None
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    for dataset, colour, suffix in _temperature_series(
            temperature_models, model=model, model_current=model_current):
        if dataset.model is None:
            continue
        if not np.array_equal(dataset.model.E_F, dataset.model_current.E_F):
            raise ValueError('Model densities and voltages must share the E_F sweep.')
        u = np.asarray(dataset.model_current.U_p, float)
        for density, label, style in ((dataset.model.p_t, r'$p_{tm}$', '-'),
                                      (dataset.model.p_f, r'$p_{fm}$', '--')):
            valid_u = _finite_positive(u) if xscale == "log" else np.isfinite(u)
            valid = valid_u & _finite_positive(density)
            ax.plot(np.where(valid, u, np.nan),
                    np.where(valid, density, np.nan),
                    ls=style if temperature_models is not None else '-',
                    label=label + suffix, **colour)
    if has_model:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    crossings = equal_density_voltage(v, p_f, p_t) if not has_model else ()
    for crossing in crossings:
        ax.axvline(crossing, ls="--", lw=1.0, color="0.5")
        ax.annotate(rf"$p_\mathrm{{t}} = p_\mathrm{{f}}$, {crossing:.2f} V",
                    (crossing, 0.02), xycoords=("data", "axes fraction"),
                    rotation=90, va="bottom", ha="right", fontsize="small",
                    color="0.4")
    _style(ax, xlabel=_U_AXIS,
           ylabel=r"charge density, $n_f$, $n_t$ (m$^{-3}$)" if has_model else _P_AXIS)
    return fig, ax


def plot_carrier_fraction(carriers, *, model=None, model_current=None,
                          temperature_models=None):
    """Parameter theta against voltage, the axes of Supplementary Fig. S19.

    By default ``Theta = p_f / p_t = mu_eff / mu_0``, an unbounded ratio;
    equal labelled trapped and free densities give ``Theta = 1``. For an
    explicitly selected free-over-total reading, equality gives one half.
    Points above 1 need more mobility than the ``mu_0`` in use; they are drawn,
    not clipped. Linear voltage against logarithmic ``Theta``; nonpositive
    values -- the rows where equation (6) turns negative -- stay in the data but
    cannot appear on a logarithmic axis.
    """
    if (model is None) != (model_current is None):
        raise ValueError('Supply both model occupations and model current.')
    if model is not None and not np.array_equal(model.E_F, model_current.E_F):
        raise ValueError('Model fractions and voltages must share the E_F sweep.')
    v, theta = np.asarray(carriers.U, float), np.asarray(carriers.theta, float)
    ok = np.isfinite(v) & _finite_positive(theta)
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_yscale("log")
    if model is None and temperature_models is None:
        if carriers.theta_model == "mobility_ratio":
            references = ((1.0, r"$p_\mathrm{t} = p_\mathrm{f}$"),)
        else:
            references = ((1.0, r"$p_\mathrm{t} \ll p_\mathrm{f}$"),
                          (0.5, r"$p_\mathrm{t} = p_\mathrm{f}$"))
    else:
        references = ()
    for level, name in references:
        ax.axhline(level, ls="--", lw=1.0, color="0.5")
        ax.annotate(name, (0.01, level), xycoords=("axes fraction", "data"),
                    va="bottom", fontsize="small", color="0.4")
    ax.plot(np.where(ok, v, np.nan), np.where(ok, theta, np.nan),
            "o", ms=4, label=r"$\Theta$")
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    for dataset, colour, suffix in _temperature_series(
            temperature_models, model=model, model_current=model_current):
        if dataset.model is None:
            continue
        if not np.array_equal(dataset.model.E_F, dataset.model_current.E_F):
            raise ValueError('Model fractions and voltages must share the E_F sweep.')
        valid = np.isfinite(dataset.model_current.U_p) & _finite_positive(dataset.model.theta_p)
        ax.plot(np.where(valid, dataset.model_current.U_p, np.nan),
                np.where(valid, dataset.model.theta_p, np.nan),
                label=r'$\Theta_m$' + suffix, **colour)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    _style(ax, xlabel=_U_AXIS, ylabel=r'Theta, $\Theta$ (-)')
    return fig, ax


def plot_fermi_dirac(relative_energy, *, thermal_energy, temperature_models=None):
    """Occupied and empty probabilities versus E-E_F on linear axes."""
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    for dataset, colour, suffix in _temperature_series(
            temperature_models, temperature=None):
        kt = thermal_energy if dataset.temperature is None else K_B * dataset.temperature / E_CHARGE
        occupied, empty = fermi_dirac_probabilities(relative_energy, thermal_energy=kt)
        ax.plot(relative_energy, occupied, label=r'$f_{\mathrm{FD}}(E)$' + suffix, **colour)
        ax.plot(relative_energy, empty, label=r'$1-f_{\mathrm{FD}}(E)$' + suffix,
                ls='--' if temperature_models is not None else '-', **colour)
    _style(ax, xlabel=r'Relative energy, $E-E_F$ (eV)',
           ylabel='Occupation probability (-)')
    return fig, ax


def plot_model_occupations(model, *, temperature_models=None):
    """Free and trapped electrons and holes versus EF on one chart.

    Nonpositive/nonfinite values leave gaps on the logarithmic axis;
    signed populations remain available in model. Returns (figure, axes).
    """
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_yscale('log')
    for dataset, colour, temperature_label in _temperature_series(temperature_models, model=model):
        for carrier, suffix, default_colour, style in (
                ('p', 't', 'C0', '-'), ('n', 't', 'C1', '-.'),
                ('p', 'f', 'C0', '--'), ('n', 'f', 'C1', ':')):
            values = getattr(dataset.model, f'{carrier}_{suffix}')
            ax.plot(dataset.model.E_F, np.where(
                np.isfinite(values) & (values > 0), values, np.nan),
                color=colour.get('color', default_colour),
                ls=style if temperature_models is not None else ('-' if suffix == 't' else '--'),
                label=rf'${carrier}_{{{suffix}}}$ ($E_F$)' + temperature_label)
    _style(ax, xlabel='', ylabel='')
    fig.tight_layout()
    return fig, ax


def plot_trapped_charge(carriers, model, *, temperature_models=None):
    """Measured/model charge pairs with a separate reversed free-electron axis."""
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_xscale('log')
    ax.set_yscale('log')
    for y, label in ((carriers.p_t, r'$p_t$ (m$^{-3}$)'),
                     (carriers.p_f, r'$p_f$ (m$^{-3}$)')):
        valid = _finite_positive(carriers.p_f, y)
        ax.plot(np.where(valid, carriers.p_f, np.nan),
                np.where(valid, y, np.nan), 'o', ms=4, label=label)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    secondary = fig.add_subplot(111, label='free_population_pair', frameon=False)
    secondary.set_yscale('log')
    secondary.xaxis.tick_top()
    secondary.xaxis.set_label_position('top')
    secondary.yaxis.set_visible(False)
    secondary.set_xlabel(r'Energy, $E_F$ (eV)')
    window_points = []
    for dataset, colour, suffix in _temperature_series(temperature_models, model=model):
        m = dataset.model
        for y, label, style in ((m.p_t, r'$p_{tm}$', '-'),
                                (m.p_f, r'$p_{fm}$', '--'),
                                (m.n_t, r'$n_{tm}$', ':')):
            valid = _finite_positive(m.p_f, y)
            ax.plot(np.where(valid, m.p_f, np.nan), np.where(valid, y, np.nan),
                    ls=style if temperature_models is not None else '-',
                    label=label + suffix, **colour)
        valid = np.isfinite(m.n_f) & _finite_positive(m.p_f)
        secondary.plot(np.where(valid, m.n_f, np.nan),
                       np.where(valid, m.p_f, np.nan),
                       label=r'$p_{fm}$' + suffix,
                       **(colour or dict(color='C5')))
        window = valid & (m.p_f >= xlim[0]) & (m.p_f <= xlim[1])
        window_points.append(np.column_stack((m.n_f[window], m.p_f[window])))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    secondary.dataLim = Bbox.null()
    for points in window_points:
        if points.size:
            secondary.update_datalim(points)
    secondary.autoscale_view()
    secondary.set_ylim(ylim)
    secondary.invert_xaxis()
    _style(ax, xlabel=r'Free charge, $n_f$ (m$^{-3}$)',
           ylabel=r'Trapped charge, $n_t$ (m$^{-3}$)')
    handles, labels = ax.get_legend_handles_labels()
    extra_handles, extra_labels = secondary.get_legend_handles_labels()
    ax.legend(handles + extra_handles, labels + extra_labels, frameon=False)
    return fig, (ax, secondary)

def plot_model_fermi_level(model, fermi, *, temperature_models=None):
    """M3 hole energy separation versus the M2 absolute free-hole density.

    Preserve the full signed energy range. Nonpositive/nonfinite densities
    leave gaps on the logarithmic concentration axis.
    """
    if not np.array_equal(model.E_F, fermi.E_F):
        raise ValueError("Occupations and energy differences must share the E_F sweep.")
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_xscale('log')
    for dataset, colour, suffix in _temperature_series(
            temperature_models, model=model, model_levels=fermi):
        pf = np.asarray(dataset.model.p_f, dtype=float)
        ax.plot(np.where(_finite_positive(pf), pf, np.nan), dataset.model_levels.delta_E_v,
                label=r'$E_F-E_v$' + suffix, **colour)
    ax.axhline(0, color='0.5', ls=':', label=r'$E_F=E_v$')
    _style(ax, xlabel=r'Free-hole concentration, $p_f$ (m$^{-3}$)',
           ylabel=r'Fermi level separation, $E_F-E_v$ (eV)')
    return fig, ax


def plot_fermi_energy(measured, model_current, model_levels, *, temperature_models=None):
    """Absolute measured/model Fermi energies versus hole-branch voltage.

    Linear axes fit the measured points; the equilibrium reference and full
    model curve remains available but does not widen the display limits.
    """
    if not np.array_equal(model_current.E_F, model_levels.E_F):
        raise ValueError('Model voltage and energy must share the E_F sweep.')
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    valid = np.isfinite(measured.U) & np.isfinite(measured.E_F)
    ax.plot(np.where(valid, measured.U, np.nan),
            np.where(valid, measured.E_F, np.nan), 'o', ms=4,
            label=r'$E_F$')
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    ax.axhline(model_levels.E_F0, color='0.5', ls='--', label=r'$E_{F0}$')
    for dataset, colour, suffix in _temperature_series(
            temperature_models, model_current=model_current, model_levels=model_levels):
        current, levels = dataset.model_current, dataset.model_levels
        if not np.array_equal(current.E_F, levels.E_F):
            raise ValueError('Model voltage and energy must share the E_F sweep.')
        valid = np.isfinite(current.U_p) & np.isfinite(levels.E_F)
        ax.plot(np.where(valid, current.U_p, np.nan),
                np.where(valid, levels.E_F, np.nan), label=r'$E_{Fm}$' + suffix, **colour)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    _style(ax, xlabel=_U_AXIS, ylabel=r'Energy, $E_F$ (eV)')
    return fig, ax


def plot_density_energy(energy, dos, carriers, measured_levels, model, derivatives,
                        *, temperature_models=None):
    """DOS and carrier densities; comparison limits follow measured series only."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    right = ax.twinx()
    ax.set_yscale('log')
    right.set_yscale('log')
    def draw(target, x, y, label, style='-', **colour):
        x, y = np.asarray(x, float), np.asarray(y, float)
        if x.shape != y.shape:
            raise ValueError('Each energy series must match its density array.')
        valid = np.isfinite(x) & _finite_positive(y)
        target.plot(np.where(valid, x, np.nan), np.where(valid, y, np.nan),
                    style, ms=3, label=label, **colour)
    e_meas = measured_levels.E_F
    draw(ax, e_meas, derivatives.measured, r'$dp/dE_F$', 'o', color='C1')
    draw(right, e_meas, carriers.p_t, r'$p_t$ (m$^{-3}$)', 'o', color='C7')
    draw(right, e_meas, carriers.p_f, r'$p_f$ (m$^{-3}$)', 'o', color='C8')
    finite = e_meas[np.isfinite(e_meas)]
    if not finite.size:
        raise ValueError('No finite measured energies to determine display limits.')
    span = np.ptp(finite)
    pad = .05 * (span if span > 0 else max(abs(finite[0]), 1.))
    xlim = finite.min() - pad, finite.max() + pad
    ylim, right_ylim = ax.get_ylim(), right.get_ylim()
    draw(ax, energy, dos, r'$g(E)$', color='C0')
    for dataset, colour, suffix in _temperature_series(
            temperature_models, model=model, density_derivative=derivatives.model):
        m = dataset.model
        for target, y, label, style, default_colour in (
                (right, m.n_t, r'$n_{tm}$', '-', 'C2'),
                (ax, dataset.density_derivative, r'$dp_m/dE_F$', '-', 'C3'),
                (ax, m.p_t, r'$p_{tm}$', '--', 'C4'),
                (ax, m.p_f, r'$p_{fm}$', ':', 'C5'),
                (ax, m.n_f, r'$n_{fm}$', '-.', 'C6')):
            draw(target, m.E_F, y, label + suffix,
                 style if temperature_models is not None else '-',
                 **(colour or dict(color=default_colour)))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    right.set_ylim(right_ylim)
    for target in (ax, right):
        target.yaxis.set_major_formatter(LogFormatterSciNotation())
    ax.set_xlabel(r'Energy, $E$, $\Delta E_F$ (eV)')
    ax.set_ylabel(r'$g(E),\ dn/dE_F$ (m$^{-3}$eV$^{-1}$)')
    right.set_ylabel(r'$n_f,\ n_t$ (m$^{-3}$)')
    ax.grid(True, which='major', alpha=.3)
    handles = list(ax.lines) + list(right.lines)
    ax.legend(handles=handles, frameon=False, loc='upper left', bbox_to_anchor=(1.16, 1.))
    fig.tight_layout()
    return fig, (ax, right)


def plot_model_current(model, *, measured=None, material=None, mu_0=None,
                       equilibrium_holes=None, temperature_models=None):
    """Hole current and negated electron current versus the hole voltage.

    Optional Ohmic and Mott–Gurney references use the supplied material,
    microscopic mobility and equilibrium free-hole density. The dimensionless
    visualisation factors ``_OHMIC_FACTOR`` and ``_MOTT_GURNEY_FACTOR`` shift
    their amplitudes while preserving logarithmic slopes of 1 and 2. Invalid
    log points leave gaps. Comparison limits are set from measurements only.
    """
    references = (material, mu_0, equilibrium_holes)
    if any(value is not None for value in references) and any(
            value is None for value in references):
        raise ValueError('Supply material, mu_0 and equilibrium_holes together.')
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_xscale("log")
    ax.set_yscale("log")
    if measured is not None:
        ok = _finite_positive(measured.V, measured.J)
        ax.plot(measured.V[ok], measured.J[ok], "o", ms=4, label=r'$j$ (A/m$^2$)')
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
    for dataset, colour, suffix in _temperature_series(temperature_models, model_current=model):
        current = dataset.model_current
        for u, j, label, style in ((current.U_p, current.J_p, r'$j_m\ (p_f)$', '-'),
                                  (current.U_p, -np.asarray(current.J_n), r'$-j_m\ (n_f)$', '--')):
            ok = _finite_positive(u, j)
            ax.plot(np.where(ok, u, np.nan), np.where(ok, j, np.nan),
                    ls=style if temperature_models is not None else '-',
                    label=label + suffix, **colour)
    if measured is None:
        xlim = ax.get_xlim()
    if material is not None:
        u = np.asarray(xlim)
        for dataset, colour, suffix in _temperature_series(
                temperature_models, model=SimpleNamespace(p_f0=equilibrium_holes)):
            ohmic = (E_CHARGE * mu_0 * dataset.model.p_f0 * u / material['L']
                     * _OHMIC_FACTOR)
            ax.plot(u, ohmic, '--', label=r'$m=1$' + suffix,
                    **(colour or dict(color='0.45')))
        mott_gurney = (9 / 8 * EPSILON_0 * material['eps_r'] * mu_0
                       * u**2 / material['L']**3 / _MOTT_GURNEY_FACTOR)
        ax.plot(u, mott_gurney, ':', color='0.45', label=r'$m=2$')
    if measured is not None:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    _style(ax, xlabel=_U_AXIS, ylabel=_J_AXIS)
    return fig, ax


def plot_model_transport_energy(model, *, temperature_models=None):
    """Voltage (left) and current density (right) versus absolute E_F.

    Both vertical axes are logarithmic with independent automatic limits.
    Nonpositive values leave gaps; the calculated arrays remain intact.
    Returns (figure, (voltage_axes, current_axes)).
    """
    fig, voltage = plt.subplots(figsize=_FIGSIZE)
    current = voltage.twinx()
    voltage.set_xlabel(r'Fermi energy, $E_F$ (eV)')
    voltage.set_ylabel(_U_AXIS)
    current.set_ylabel(_J_AXIS)
    for ax in (voltage, current):
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(LogFormatterSciNotation())
    for dataset, colour, suffix in _temperature_series(temperature_models, model_current=model):
        m = dataset.model_current
        for ax, values, label, default_colour, style in (
                (voltage, m.U_n, r'$U\ (n_t)$', 'C0', '-'),
                (voltage, m.U_p, r'$U\ (p_t)$', 'C1', '-.'),
                (current, m.J_n, r'$j\ (n_f)$', 'C0', '--'),
                (current, m.J_p, r'$j\ (p_f)$', 'C1', ':')):
            valid = np.isfinite(m.E_F) & _finite_positive(values)
            ax.plot(m.E_F, np.where(valid, values, np.nan),
                    label=label + suffix, color=colour.get('color', default_colour),
                    ls=style if temperature_models is not None else ('-' if ax is voltage else '--'))
    voltage.grid(True, which='major', alpha=0.3)
    lines = voltage.lines + current.lines
    voltage.legend(lines, [line.get_label() for line in lines], frameon=False)
    fig.tight_layout()
    return fig, (voltage, current)


def plot_hole_current_semilog(model, *, measured, temperature_models=None):
    """Measured and model hole current with linear U and logarithmic j.

    Preserve signed voltages; nonpositive currents cannot be displayed.
    Invalid model rows leave gaps, without changing the calculated arrays.
    """
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_yscale("log")
    v, j = np.asarray(measured.V, float), np.asarray(measured.J, float)
    ok = np.isfinite(v) & _finite_positive(j)
    ax.plot(v[ok], j[ok], "o", ms=4, label=r"$j$ (A/m$^2$)")
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    for dataset, colour, suffix in _temperature_series(temperature_models, model_current=model):
        u, j = np.asarray(dataset.model_current.U_p, float), np.asarray(dataset.model_current.J_p, float)
        ok = np.isfinite(u) & _finite_positive(j)
        ax.plot(np.where(ok, u, np.nan), np.where(ok, j, np.nan),
                label=r"$j_m\ (p_f)$" + suffix, **colour)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    _style(ax, xlabel=_U_AXIS, ylabel=_J_AXIS)
    return fig, ax


def plot_dos(energy, *, E_v, E_c, m_eff_h, m_eff_e, N_t, E_t, T_t):
    """Plot the two parabolic bands and the localized trap DOS.

    Energy is in eV on the vacuum scale. Mark the band edges and trap
    maximum. DOS_FLOOR and underflowed zeros are omitted on logarithmic
    axes. All numerical parameters are passed through to the backend.
    Returns (figure, axes)."""
    e = np.asarray(energy, dtype=float)
    traps = dict(N_t=N_t, E_t=E_t, T_t=T_t)
    # Fixed colours: a band absent from this energy range must not repaint
    # the series that remain.
    series = ((valence_band_dos(e, E_v=E_v, m_eff_h=m_eff_h),
               r"$g_\mathrm{h}$, valence band", "C0"),
              (conduction_band_dos(e, E_c=E_c, m_eff_e=m_eff_e),
               r"$g_\mathrm{e}$, conduction band", "C1"),
              (trap_dos(e, **traps), r"$g_\mathrm{t}$, trap", "C2"))
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.set_yscale("log")
    peaks = []
    for values, label, colour in series:
        drawn = np.where(values > DOS_FLOOR, values, np.nan)
        if not np.isfinite(drawn).any():      # wholly outside this energy range
            continue
        peaks.append(np.nanmax(drawn))
        ax.plot(e, drawn, lw=1.7, color=colour, label=label)
    low, high = np.nanmin(e), np.nanmax(e)
    for level, name in ((E_v, "$E_v$"), (E_t, "$E_t$"), (E_c, "$E_c$")):
        if not low <= level <= high:      # off the plotted range, so not marked
            continue
        ax.axvline(level, ls="--", lw=1.0, color="0.5")
        ax.annotate(f"{name} = {level:g} eV", (level, 0.02),
                    xycoords=("data", "axes fraction"), rotation=90,
                    va="bottom", ha="right", fontsize="small", color="0.4")
    ax.set_xlim(low, high)                    # the edge markers must not widen it
    top = max(peaks, default=np.nan)
    if np.isfinite(top) and top > 0:      # else every row is floor or nan
        ax.set_ylim(top * 1e-21, top * 10)
    _style(ax, xlabel=_E_AXIS, ylabel=_G_AXIS)
    return fig, ax
