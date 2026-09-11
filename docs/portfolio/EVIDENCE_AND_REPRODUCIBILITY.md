# Evidence, model scope and reproducibility

## Source groups and what they support

| Evidence group | Supports | Does not establish |
|---|---|---|
| Existing `comsol/` and `docs/model_validation.md` records | Earlier baseline setup, flow-boundary correction, documented mesh/energy checks | Those checks applying automatically to the later 0.30 × 0.70 mm geometry |
| Corrected 45-case flow/TIM table | Complete parameter grid, split labels, temperature/pressure/power records | Complete final-geometry energy balance; exact final trained-model provenance |
| Five off-grid prediction/COMSOL comparisons | Recalculation of reported prediction errors and all five temperature classifications | A newly reproduced GPR training run or general extrapolation accuracy |
| Three COMSOL confirmation exports | Reported final Pareto candidates and hydraulic/thermal trade-offs | Experimental performance, a unique global optimum, full-system electrical pump power |

The current repository consolidation joins the existing surrogate-validation and final-results branches. Source bytes and interpretation remain separate from new presentation material. See [the manifest](source_manifest.json) and [release notes](RELEASE_NOTES.md).

## Model and metric definitions

The final result package describes ten 0.30 × 0.70 mm water channels, 100 W heat load and 25°C inlet. The sampled variables are total flow (0.10–0.30 L/min), TIM thickness (0.05–0.15 mm) and conductivity (1.5–6 W/(m·K)). The early root README's 0.50 × 0.50 mm geometry is an older baseline. This release does not silently reconcile unverified dimensions or replace the original COMSOL parameter files.

System thermal resistance is `(Tmax_chip - Tin)/P_heat`. Hydraulic pumping power is `dp_Pa * flow_Lmin / 60000`, not electrical input. Temperature errors are emphasized in °C: percentage error referenced to Celsius temperature is scale-dependent. The supplied metric CSV retains its historical temperature MAPE but that value is not used as the main accuracy claim.

In the five-case comparison, `predicted_pump_power_W` is consistent with predicted pressure multiplied by prescribed flow. `independent_pump_model_prediction_W` is a separate column. The reported pumping-power metric uses the former. Likewise, system resistance and maximum chip temperature are algebraically linked at fixed heat load and inlet temperature; they are not five fully independent accuracy demonstrations.

## What can be reproduced now

`python scripts/review_project1.py` recalculates the grid and split checks, data identities, five-case errors and pass/fail agreement, and final-design trade-off from the stored CSVs. It does not execute a high-fidelity solver or regenerate predictions.

The inherited `src/train_models.py` is an early linear/random-forest/gradient-boosting benchmark with a different feature schema, not the final GPR pipeline. The separately supplied historical training package contains a GPR candidate but also selects models using the nine-row development holdout. This organization task leaves training/model code unchanged and does not claim to recreate the final selected checkpoint, full Pareto cloud, runtime speedup, or deployed Streamlit inference application.

## Unresolved evidence and release limits

The 45-case core table marks energy-balance data unavailable for all rows. Final confirmation and five-case validation exports likewise lack all energy-balance terms. Hydraulic conservation checks are useful but do not substitute for heat conservation. The final confirmation README explicitly calls for a recommended-design energy-balance result against the <2% project criterion; preserve that requirement.

The optimized TIM values (0.05 mm / 6 W/(m·K)) are recorded optimization metadata, not columns in the three raw confirmation exports. Final-geometry mesh independence and complete energy-balance evidence should be attached from the matching COMSOL runs. Do not infer them from the earlier square-channel validation.

For a reproducible prediction release, attach the final fitted GPR model or deterministic training pipeline, final training configuration, software versions and split/provenance record; then regenerate and compare predictions while preserving the independent checks. Until then, the portfolio demonstrates a documented simulation/surrogate design study with auditable result tables, not a one-command recreation of every original analysis.

## Public-job-search review

The GitHub repository is private at organization time. No visibility, collaborator or license change is part of this work. Before making a public portfolio, review the complete repository history and source rights, supply any required license decision, resolve the missing artifacts or keep the limitations visible, and explicitly authorize public visibility. Do not publish virtual environments, credentials, unrelated research, or private local-workspace content.
