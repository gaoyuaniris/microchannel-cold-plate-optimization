# Mesh and energy validation

## Conclusion

**Overall status: PASS**

At 0.25 L/min, the **normal mesh** passes all convergence,
flow-conservation, and COMSOL-integrated energy-balance criteria relative to
the **finer mesh**. Recommended production mesh: **normal**.

## Design-point results

| Mesh | Tmax (°C) | Rth (K/W) | Pressure drop (Pa) | Pumping power (W) | Outlet T (°C) | Flow imbalance (%) |
|---|---|---|---|---|---|---|
| coarse | 86.2691 | 0.6127 | 5150.9162 | 0.0215 | 29.8062 | 0.0000 |
| normal | 86.3166 | 0.6132 | 5146.4860 | 0.0214 | 29.8044 | 0.0000 |
| finer | 86.2235 | 0.6122 | 5146.6632 | 0.0214 | 29.7771 | 0.0000 |

## Normal-to-Finer convergence checks

| Metric | Difference | Limit | Unit | Pass |
|---|---|---|---|---|
| max_chip_temperature_C | 0.0930 | 0.5000 | °C | True |
| thermal_resistance_K_W | 0.1519 | 1.0000 | % | True |
| pressure_drop_Pa | 0.0034 | 3.0000 | % | True |
| pumping_power_W | 0.0034 | 3.0000 | % | True |
| outlet_temperature_C | 0.0273 | 0.2000 | °C | True |

## COMSOL-integrated balance checks

| Flow (L/min) | Heat source (W) | Heat error (%) | Energy error (%) | Pass |
|---|---|---|---|---|
| 0.1000 | 99.9695 | 0.3742 | 0.3744 | True |
| 0.1500 | 99.9678 | 0.3171 | 0.3175 | True |
| 0.2000 | 99.9439 | 0.5903 | 0.5914 | True |
| 0.2500 | 99.9543 | 0.4600 | 0.4619 | True |
| 0.3000 | 99.9262 | 0.6463 | 0.6496 | True |

At the design point, the integrated energy-balance error is
0.4619%, below the
2% acceptance limit.

## Acceptance criteria

- Tmax absolute difference < 0.5 °C
- Thermal-resistance difference < 1%
- Pressure-drop difference < 3%
- Pumping-power difference < 3%
- Outlet-temperature absolute difference < 0.2 °C
- Flow imbalance < 0.5%
- COMSOL-integrated energy-balance error < 2%

## Reproduce

```bash
python3 scripts/analyze_mesh_study.py
```

Raw sources:

- `comsol/exported_results/validation/mesh_sweep_results.csv`
- `comsol/exported_results/validation/energy_balance_validation.csv`

Element counts and solve times were not present in the supplied COMSOL exports,
so they are not reported or estimated.
