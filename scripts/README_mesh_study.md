# Earlier-baseline COMSOL validation workflow

This workflow converts the raw COMSOL mesh-sweep and global energy-balance
exports into clean, GitHub-ready tables, figures, and a validation report.

This workflow checks the earlier 0.50 × 0.50 mm square-channel baseline. It does not establish mesh convergence or energy balance for the final 0.30 × 0.70 mm study; see [validation scope](../docs/STUDY_AND_VALIDATION.md).

The baseline validation uses:

- design flow: 0.25 L/min
- heat load: approximately 100 W
- inlet temperature: 25 °C
- meshes: coarse, normal, and finer
- energy validation mesh: normal

No simulation values are generated or estimated. The script stops if a
required COMSOL value or column is missing.

## Repository layout

```text
comsol/exported_results/validation/
├── mesh_sweep_results.csv
└── energy_balance_validation.csv

scripts/
├── analyze_mesh_study.py
└── README_mesh_study.md

data/processed/validation/
├── mesh_results_tidy.csv
├── convergence_metrics.csv
├── energy_balance_summary.csv
├── design_point_summary.csv
└── validation_decision.csv

figures/validation/
├── tmax_vs_flow_rate.png
├── pressure_drop_vs_flow_rate.png
├── pumping_power_vs_flow_rate.png
└── energy_balance_error_vs_flow_rate.png

report/validation/
└── mesh_energy_validation.md
```

Raw COMSOL exports remain unchanged. The processed tables are flat CSV files
with one observation per row, making them suitable for Python, Excel, and
future machine-learning work.

## Run the analysis

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 scripts/analyze_mesh_study.py
```

The final terminal message should report:

```text
Validation status: PASS
Recommended mesh: normal
Reference mesh: finer
```

## What the script checks

At 0.25 L/min, the normal mesh must satisfy:

| Check | Requirement |
|---|---:|
| Tmax absolute difference from finer | < 0.5 °C |
| Thermal-resistance difference from finer | < 1% |
| Pressure-drop difference from finer | < 3% |
| Pumping-power difference from finer | < 3% |
| Outlet-temperature difference from finer | < 0.2 °C |
| Inlet/outlet flow imbalance | < 0.5% |
| COMSOL-integrated energy-balance error | < 2% |

The energy error is calculated directly from COMSOL's integrated residual:

```text
energy error = |energy-balance residual| / |total heat source| × 100%
```

It does not reconstruct energy balance from average outlet temperature.

## Using updated exports

Replace the two files in `comsol/exported_results/validation/` with new COMSOL
exports that retain the same table expressions, then rerun the script. The
processed tables, figures, and Markdown report will be regenerated.

Use different source or output paths with:

```bash
python3 scripts/analyze_mesh_study.py \
  --mesh-input path/to/mesh_results.csv \
  --energy-input path/to/energy_results.csv \
  --processed-dir path/to/processed \
  --figures-dir path/to/figures \
  --report path/to/report.md
```

## Current limitation

The supplied mesh export does not contain element counts or solver times, so
the workflow does not invent them or create element-count/solve-time plots.
Export those fields from COMSOL before adding computational-cost comparisons.
