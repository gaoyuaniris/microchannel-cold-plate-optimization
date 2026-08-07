# AI-Assisted Microchannel Cold-Plate Design Tool

A GitHub-ready portfolio project combining COMSOL conjugate heat-transfer simulation, microchannel liquid cooling, Python data processing, machine-learning surrogate models, and multi-objective optimization.

## Objective

Design and analyze a water-cooled microchannel cold plate for a compact high-heat-flux electronic device. Evaluate maximum chip temperature, thermal resistance, pressure drop, pumping power, and temperature uniformity, then use a surrogate model to accelerate design exploration.

## Baseline design

| Parameter | Baseline |
|---|---:|
| Chip | 10 × 10 × 0.5 mm |
| TIM | 10 × 10 × 0.10 mm, 3 W/(m·K) |
| Copper spreader | 12 × 12 × 1 mm |
| Copper cold plate | 30 × 30 × 3 mm |
| Channels | 10 parallel channels |
| Channel size | 0.50 × 0.50 × 25 mm |
| Coolant | Water |
| Inlet temperature | 25 °C |
| Chip power | 100 W |
| Total flow | 0.20 L/min |

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python hand_calculations/baseline_calculations.py
pytest
```

Place COMSOL-exported CSV files in `comsol/exported_results/`, then run:

```bash
python -m src.load_data
python -m src.train_models
streamlit run app/streamlit_app.py
```

## Current COMSOL results

Preliminary Day 3 baseline and flow-sweep exports are available in:

- [`comsol/exported_results/day03/`](comsol/exported_results/day03/)
- [`figures/day03/`](figures/day03/)

The results show the expected thermal-hydraulic tradeoff: increasing flow
reduces maximum chip temperature and thermal resistance while increasing
pressure drop and pumping power. The ten-channel outlet area is correct,
but the integrated outlet flow remains lower than the requested flow-rate
parameter. See the
[Day 3 validation notes](comsol/exported_results/day03/README.md) before
using these values for optimization.

## Surrogate validation

The trained surrogate was checked against five independent, off-grid COMSOL
cases within the sampled design ranges. All five outputs passed their defined
acceptance criteria, and the model correctly classified all five cases against
the 85 °C maximum-chip-temperature limit.

Maximum chip-temperature error was 0.0994 °C, while pressure-drop and pumping-
power MAPE were both 0.0466%. See the [validation report](report/validation/surrogate/README.md),
[analysis workbook](report/validation/surrogate/coldplate_surrogate_validation_analysis.xlsx),
and [comparison data](data/processed/validation/surrogate/coldplate_validation_comparison.csv)
for the complete results.

## Roadmap

1. Complete baseline calculations.
2. Build and verify a stationary COMSOL model.
3. Perform mesh-independence and energy-balance checks.
4. Run parameter sweeps.
5. Export one row per case.
6. Build the Python data pipeline.
7. Train surrogate models.
8. Generate a Pareto frontier.
9. Re-run selected designs in COMSOL.
10. Package the results for interviews and applications.
