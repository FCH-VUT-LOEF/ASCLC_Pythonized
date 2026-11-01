"""Temperature controls and chart integration, using existing notebook inputs."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import numpy as np
import pytest

import asclc_plotting as plotting
from asclc_workflow import run_temperature_models, temperature_range


@pytest.mark.parametrize('start,stop,step,expected', [
    (299, 303, 2, [299, 301, 303]),
    (303, 299, -2, [303, 301, 299]),
    (299, 302, 2, [299, 301]),
    (299, 299, 1, [299]),
    (299, 299.3, .1, [299, 299.1, 299.2, 299.3]),
])
def test_range_endpoint_and_direction(start, stop, step, expected):
    np.testing.assert_allclose(temperature_range(start=start, stop=stop, step=step), expected)


@pytest.mark.parametrize('start,stop,step', [
    (0, 299, 1), (299, np.inf, 1), (299, 300, 0),
    (299, 300, -1), (300, 299, 1), (299, 300, np.nan),
])
def test_invalid_ranges(start, stop, step):
    with pytest.raises(ValueError):
        temperature_range(start=start, stop=stop, step=step)


def test_workflow_passes_temperature_and_preserves_all_other_inputs():
    """Check orchestration without altering or recomputing the physical equations."""
    n = json.loads(Path('notebooks/asclc.ipynb').read_text())
    scope = {'project_root': Path.cwd()}
    exec(''.join(n['cells'][3]['source']), scope)
    material, params = scope['material'], scope['params']
    original_material, original_params = material.copy(), params.copy()
    # Use the notebook's grid definitions verbatim.
    grid_code = ast.parse(''.join(n['cells'][20]['source']))
    grids = [node for node in grid_code.body if isinstance(node, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id in {'model_energy', 'model_fermi'}
                     for t in node.targets)]
    scope['np'] = np
    exec(compile(ast.Module(body=grids, type_ignores=[]), '<grids>', 'exec'), scope)
    energy, ef = scope['model_energy'], scope['model_fermi']
    energy_copy, ef_copy = energy.copy(), ef.copy()
    model = SimpleNamespace(E_F=ef, p_s=np.ones_like(ef))
    with patch('asclc_workflow.run_model_occupations', return_value=model) as occupation, \
         patch('asclc_workflow.run_model_current') as current, \
         patch('asclc_workflow.run_model_fermi_level'), \
         patch('asclc_workflow.run_model_mobility'):
        results = run_temperature_models(energy, ef, material=material, params=params,
                                         start=299, stop=303, step=2)
    assert [item.temperature for item in results] == [299, 301, 303]
    assert [call.kwargs['temperature'] for call in occupation.call_args_list] == [299, 301, 303]
    np.testing.assert_allclose([call.kwargs['gamma'] for call in current.call_args_list],
                               params['T_t'] / np.array([299, 301, 303]))
    for call in occupation.call_args_list:
        assert call.args[0] is energy and call.args[1] is ef
        assert call.kwargs['material'] is material and call.kwargs['params'] is params
    assert material == original_material and params == original_params
    np.testing.assert_array_equal(energy, energy_copy)
    np.testing.assert_array_equal(ef, ef_copy)


@pytest.fixture(scope='module')
def chart_inputs():
    """Execute the actual notebook at its configured temperature and grids."""
    notebook = json.loads(Path('notebooks/asclc.ipynb').read_text())
    scope = {}
    for cell in notebook['cells']:
        source = ''.join(cell['source'])
        if cell['cell_type'] == 'code' and 'export_results(result,' not in source:
            exec(compile(source, '<notebook>', 'exec'), scope)
    bundle = SimpleNamespace(temperature=scope['experiment']['T'], model=scope['model'],
                             model_current=scope['model_current'], model_levels=scope['model_levels'],
                             model_mobility=scope['model_mobility'],
                             density_derivative=scope['density_derivatives'].model)
    plt.close('all')
    yield scope, bundle
    plt.close('all')


def chart_calls(s):
    return [
        (plotting.plot_model_current, (s['model_current'],), dict(measured=s['result'])),
        (plotting.plot_hole_current_semilog, (s['model_current'],), dict(measured=s['result'])),
        (plotting.plot_carrier_densities, (s['carriers'],), dict(model=s['model'], model_current=s['model_current'])),
        (plotting.plot_carrier_densities, (s['carriers'],), dict(model=s['model'], model_current=s['model_current'], xscale='log')),
        (plotting.plot_carrier_fraction, (s['carriers'],), dict(model=s['model'], model_current=s['model_current'])),
        (plotting.plot_effective_mobility, (s['result'], s['mobility']), dict(mu_0=s['params']['mu_0'], model_mobility=s['model_mobility'], model_current=s['model_current'])),
        (plotting.plot_trapped_charge, (s['carriers'], s['model']), {}),
        (plotting.plot_fermi_energy, (s['measured_levels'], s['model_current'], s['model_levels']), {}),
        (plotting.plot_density_energy, (s['dos_plot_energy'], s['total_dos'](s['dos_plot_energy'], **s['dos']), s['carriers'], s['measured_levels'], s['model'], s['density_derivatives']), {}),
        (plotting.plot_model_occupations, (s['model'],), {}),
        (plotting.plot_model_transport_energy, (s['model_current'],), {}),
        (plotting.plot_model_fermi_level, (s['model'], s['model_levels']), {}),
        (plotting.plot_fermi_dirac, (s['model_energy'] - s['params']['E_F0'],), dict(thermal_energy=s['K_B'] * s['experiment']['T'] / s['E_CHARGE'])),
    ]


def test_single_temperature_reproduces_chart_arrays_and_bounds(chart_inputs):
    s, bundle = chart_inputs
    for function, args, kwargs in chart_calls(s):
        baseline, _ = function(*args, **kwargs)
        sweep, _ = function(*args, **kwargs, temperature_models=[bundle])
        for a, b in zip(baseline.axes, sweep.axes, strict=True):
            np.testing.assert_allclose(a.get_xlim(), b.get_xlim())
            np.testing.assert_allclose(a.get_ylim(), b.get_ylim())
            assert a.get_xscale() == b.get_xscale() and a.get_yscale() == b.get_yscale()
            # Density/energy draws measurements first, so ordering is shared.
            for original, selected in zip(a.lines, b.lines, strict=True):
                np.testing.assert_allclose(original.get_xydata(), selected.get_xydata(), equal_nan=True)
        plt.close(baseline)
        plt.close(sweep)


def test_cold_blue_hot_red_independent_of_selection_order():
    models = [SimpleNamespace(temperature=t) for t in (303, 301, 299)]
    series = list(plotting._temperature_series(models))
    assert series[0][1]['color'] == to_rgba('red')
    assert series[-1][1]['color'] == to_rgba('blue')
    assert series[1][2] == ', 301 K'


def test_comparison_bounds_ignore_extra_model_curves(chart_inputs):
    s, bundle = chart_inputs
    # Extreme displayed model coordinates are fixtures, not a recalculation.
    m = bundle.model_current
    extreme = SimpleNamespace(**vars(bundle))
    extreme.temperature = 303
    extreme.model_current = SimpleNamespace(**vars(m))
    extreme.model_current.U_p = m.U_p * 1e20
    extreme.model_current.J_p = m.J_p * 1e20
    for function, args, kwargs in chart_calls(s)[:9]:
        baseline, _ = function(*args, **kwargs, temperature_models=[bundle])
        sweep, _ = function(*args, **kwargs, temperature_models=[bundle, extreme])
        for a, b in zip(baseline.axes, sweep.axes, strict=True):
            np.testing.assert_allclose(a.get_xlim(), b.get_xlim())
            np.testing.assert_allclose(a.get_ylim(), b.get_ylim())
        plt.close(baseline)
        plt.close(sweep)
