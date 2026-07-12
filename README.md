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
