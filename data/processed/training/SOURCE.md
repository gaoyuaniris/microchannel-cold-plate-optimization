# Corrected Project 1 flow/TIM dataset

`coldplate_ml_core_45.csv` is copied byte-for-byte from the supplied corrected ML preparation package. Its upstream export was named `45 data for training(2).csv`; the full raw training export is not added in this consolidation. Superseded exports with inconsistent requested/actual flow are not substituted for this file.

Fixed conditions: ten 0.30 × 0.70 mm channels, 100 W, 25°C water inlet. The complete grid contains five flows (0.10, 0.15, 0.20, 0.25, 0.30 L/min), three TIM thicknesses (0.05, 0.10, 0.15 mm), and three conductivities (1.5, 3, 6 W/(m·K)). Retained labels assign 36 rows to `train_cv` and nine 0.25 L/min rows to `test_holdout`. Group labels preserve flow-level cross-validation intent; no scaling or fitting was performed in this consolidation.

The [original preparation notes](original_preparation_notes.txt) are preserved as a historical source. They label the data suitable for **preliminary** modeling and report hydraulic checks, while explicitly requiring missing energy-balance results before a full final dataset release. Every row has `energy_balance_available=0`; do not interpret `hydraulic_qc_pass=1` as complete thermal validation. Nineteen of 45 rows meet the temperature criterion; retain the other rows as infeasible design evidence.

The preparation notes call the nine-row set an untouched holdout. However, the separately supplied historical benchmark script ranks candidate models by that set's RMSE. Any benchmark using that ranking treats it as a model-selection set, not an untouched final test. The separate five-case off-grid prediction/COMSOL table is therefore reported independently. This package does not establish which serialized checkpoint produced that table.

In this project, system thermal resistance is `(Tmax_chip_C - 25)/100` in K/W. Hydraulic power is `pressure_drop_Pa * flow_rate_Lmin / 60000` in W. This is different from Project 2's base-to-mean-coolant resistance. Do not mix the two projects' definitions or data.

File provenance and Git blob IDs are listed in [the evidence manifest](../../../docs/portfolio/source_manifest.json).
