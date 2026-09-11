# Study methods and validation evidence

This record connects the final flow/TIM study to its datasets, surrogate comparisons, and COMSOL confirmation runs. It distinguishes agreement with CFD from experimental validation and identifies which numerical checks are available for each model configuration.

## Final study configuration

The study uses stationary conjugate heat transfer in COMSOL 6.3 for a chip → explicit TIM → copper spreader → water-cooled cold plate heat path.

| Quantity | Final-study condition |
|---|---|
| Heat load / inlet temperature | 100 W / 25°C |
| Channels | Ten parallel channels, 0.30 mm wide × 0.70 mm high |
| Hydraulic diameter | 0.420 mm |
| Total flow | 0.10, 0.15, 0.20, 0.25, 0.30 L/min |
| TIM thickness | 0.05, 0.10, 0.15 mm |
| TIM conductivity | 1.5, 3, 6 W/(m·K) |
| Thermal inlet/outlet | Inflow + Outflow, as recorded in preparation notes |
| Temperature criterion | Maximum chip temperature ≤85°C, a project-defined limit |

Configuration sources: [preparation notes](../data/processed/training/original_preparation_notes.txt) and [final-result package](../results/final_engineering_results/README.md). Earlier 0.50 × 0.50 mm channel files describe a different baseline.

System thermal resistance is `Rth = (Tmax − Tin) / Qheat`. Hydraulic pumping power is `P = Δp × Vdot`, or `pressure_drop_Pa × flow_rate_Lmin / 60000` in watts. This excludes pump efficiency and other cooling-loop components.

## Dataset and split provenance

The [45-case table](../data/processed/training/coldplate_ml_core_45.csv) contains the complete 5 × 3 × 3 flow/thickness/conductivity grid. Nineteen cases satisfy the temperature criterion; the remaining 26 are retained as infeasible design evidence. The [source record](../data/processed/training/SOURCE.md) identifies the corrected upstream export and preserved split labels.

Thirty-six rows at 0.10, 0.15, 0.20, and 0.30 L/min are labeled `train_cv`; nine rows at 0.25 L/min are labeled `test_holdout`. The preparation notes recommend grouping cross-validation by flow level and fitting preprocessing only within training folds. These recommendations do not establish a recovered cross-validation execution record.

All rows carry `hydraulic_qc_pass=1` and `energy_balance_available=0`. The preparation notes report a maximum inlet/outlet flow imbalance of 0.445272%; complete final-configuration thermal energy-balance data are still absent.

## Surrogate development and model selection

The preparation notes name polynomial Ridge, Gaussian Process, Gradient Boosting, and Random Forest as comparison candidates. The final-result package describes a Gaussian-process surrogate study. A historical benchmark, documented in the [provenance notes](../data/processed/training/SOURCE.md), ranked candidate models using the nine-row holdout's RMSE; that set therefore served model selection rather than an untouched final test.

The final fitted checkpoint, exact training configuration, and numerical cross-validation comparison have not been recovered in this repository. No model-ranking scores or speedup are inferred. The inherited `src/train_models.py` uses a different schema and is not the final GPR training pipeline.

## Five off-grid COMSOL comparisons

The [case-level comparison table](../data/processed/validation/surrogate/coldplate_validation_comparison.csv) contains five additional parameter combinations inside the sampled ranges. They are distinct from the 45-case grid; their stored predictions are compared with separate COMSOL results. This supports an off-grid interpolation check, without establishing that these cases were untouched throughout all model-selection decisions.

| Output | Mean absolute error | Maximum absolute error |
|---|---:|---:|
| Maximum chip temperature | 0.0507°C | 0.0994°C |
| Mass-weighted outlet temperature | 0.1266°C | 0.1573°C |
| Pressure drop | 2.79 Pa | 5.01 Pa |

Pressure-drop MAPE is 0.0466%. Temperature pass/fail classifications agree for all five cases: V1/V5 fail; V2/V3/V4 pass. The reported maximum inlet/outlet flow imbalance is 0.361%. See the [metric CSV](../data/processed/validation/surrogate/coldplate_validation_metrics_summary.csv) and [comparison report](../report/validation/surrogate/README.md).

Temperature errors are reported in °C rather than Celsius-based percentage accuracy. Rth is algebraically linked to Tmax; the reported pumping-power prediction uses predicted pressure times prescribed flow. Those derived outputs are not independent accuracy demonstrations. Five cases do not establish extrapolation performance.

## Three selected-design confirmations

The [confirmation table](../results/final_engineering_results/data/final_selected_designs_comsol_confirmed.csv) and [raw COMSOL exports](../results/final_engineering_results/data/raw_comsol/) record three selected candidates:

| Candidate | Flow (L/min) | Tmax (°C) | Hydraulic power (mW) |
|---|---:|---:|---:|
| Minimum temperature | 0.300 | 60.618 | 54.706 |
| Balanced knee point | 0.188 | 64.725 | 19.949 |
| Minimum pumping power | 0.100 | 71.790 | 4.947 |

The balanced candidate reduces hydraulic power by 63.5% versus the minimum-temperature candidate for a 4.11°C temperature increase, retaining 20.27°C margin. These comparisons are reproduced in the [trade-off summary](../results/final_engineering_results/data/engineering_tradeoff_summary.csv).

The two extreme candidates coincide with training-grid endpoints; they are confirmation runs, not additional off-grid tests. The 0.05 mm / 6 W/(m·K) TIM setting is optimization metadata, absent from the raw confirmation columns. The complete Pareto search and knee-selection calculation are not reproduced here; the selected point is not claimed as a unique global optimum.

## Mesh and energy evidence

Two earlier reports differ at their stated 0.25 L/min condition: [model-validation notes](model_validation.md) report normal-mesh Tmax 87.704°C and 0.0731% energy error, whereas the [CSV-backed report](../report/validation/mesh_energy_validation.md) reports 86.3166°C and 0.4619%. Their configuration/revision difference remains unresolved. Neither establishes final-geometry convergence; mesh element counts and solve times are also unavailable.

The final training, off-grid, and confirmation packages lack complete final-configuration energy-balance terms. Attach matching mesh-refinement results and integrated heat-source/boundary-flux balances, including the recommended candidate against the <2% project criterion. Surrogate-to-CFD agreement cannot establish the CFD model's physical accuracy or measured hardware performance.

## Reproduce the stored-result checks

Run `python scripts/review_project1.py` from the repository root. It checks source hashes, grid/split structure, derived identities, five-case errors, and the selected-design trade-off using stored data. It does not run COMSOL, retrain the surrogate, or regenerate the optimization search.
