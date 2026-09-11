# Microchannel Cold-Plate Design for Electronics Cooling

**Yuan Gao · COMSOL 6.3 · Heat transfer and CFD · Python · Gaussian-process surrogate modeling**

A simulation-based study of cooling a **100 W electronic chip** through a **TIM, copper spreader and water-cooled microchannel cold plate**. The goal is to keep the chip below **85°C** while understanding how coolant flow and TIM properties affect temperature, pressure drop and hydraulic pumping power.

**Selected balanced candidate: 64.73°C at 0.188 L/min.** Compared with the confirmed minimum-temperature candidate at 0.300 L/min, it uses **63.5% less hydraulic pumping power** for a **4.11°C temperature increase**, retaining **20.27°C of thermal margin**.

[Final results and raw exports](results/final_engineering_results/) · [Study and validation](docs/STUDY_AND_VALIDATION.md) · [Data and reproducibility](docs/portfolio/EVIDENCE_AND_REPRODUCIBILITY.md)

## Engineering decision

![Three COMSOL-confirmed candidates: maximum chip temperature versus hydraulic pumping power](results/final_engineering_results/figures/confirmed_thermal_hydraulic_tradeoff.png)

*100 W heat load, 25°C inlet water, ten 0.30 × 0.70 mm channels. The line connects three COMSOL-confirmed candidates; it is not the full surrogate Pareto frontier. Their shared TIM setting, 0.05 mm and 6 W/(m·K), is retained as optimization metadata.*

| Confirmed candidate | Flow (L/min) | Chip Tmax (°C) | Rth (K/W) | Pressure drop (kPa) | Hydraulic power (mW) |
|---|---:|---:|---:|---:|---:|
| Minimum temperature | 0.300 | 60.62 | 0.3562 | 10.94 | 54.71 |
| **Balanced candidate** | **0.188** | **64.73** | **0.3973** | **6.37** | **19.95** |
| Minimum pumping power | 0.100 | 71.79 | 0.4679 | 2.97 | 4.95 |

All three meet the project's 85°C temperature criterion. The balanced candidate is a useful compromise when thermal margin and hydraulic cost both matter; the lowest-power candidate remains an alternative when less thermal margin is acceptable. Candidate names follow the original study and do not establish a unique global optimum.

Sources: [confirmed-design CSV](results/final_engineering_results/data/final_selected_designs_comsol_confirmed.csv), [raw COMSOL confirmation files](results/final_engineering_results/data/raw_comsol/) and [trade-off calculations](results/final_engineering_results/data/engineering_tradeoff_summary.csv). Hydraulic power is **Δp × volumetric flow**; electrical pump efficiency and external loop losses are outside this comparison.

## What I modeled and analyzed

**Heat path:** 100 W chip → TIM → copper spreader → copper cold plate → water.

The 3D stationary conjugate heat-transfer study connects solid conduction and coolant flow. Python post-processing converts COMSOL outputs into chip temperature, chip-to-inlet thermal resistance, outlet temperature, pressure drop and pumping power.

| Study input | Final-study setting |
|---|---|
| Coolant / inlet temperature / chip load | Water / 25°C / 100 W |
| Channel cross-section / count | 0.30 × 0.70 mm / 10 parallel channels |
| Total flow | 0.10, 0.15, 0.20, 0.25, 0.30 L/min |
| TIM thickness | 0.05, 0.10, 0.15 mm |
| TIM conductivity | 1.5, 3, 6 W/(m·K) |
| Design dataset | **45 combinations**; 19 meet the 85°C criterion |

The workflow was **COMSOL parameter study → surrogate comparison and GPR selection → five off-grid checks → Pareto screening → three COMSOL confirmation runs**. The 45-case dataset includes thermally infeasible designs, so the study captures the boundary of acceptable performance as well as promising candidates.

The design lesson is that additional flow carries a pumping penalty, while the TIM remains an important part of the thermal path. The selected candidates use the thin, high-conductivity edge of the studied TIM range; this is an idealized thermal study, with manufacturing and contact uncertainties left for later evaluation.

## Surrogate-to-COMSOL comparison

Five separate off-grid cases tested new flow/TIM combinations inside the studied ranges. Recalculation of the preserved prediction and COMSOL records gives:

| Quantity | Result across five cases |
|---|---:|
| Mean absolute chip-temperature error | **0.051°C** |
| Maximum absolute chip-temperature error | **0.099°C** |
| Pressure-drop mean absolute percentage error | **0.0466%** |
| Agreement with the 85°C pass/fail criterion | **5 / 5 cases** |

![Recorded surrogate predictions and COMSOL chip temperatures for five off-grid cases](figures/validation/surrogate/validation_Tmax_comparison.png)

*V1 and V5 exceed 85°C; V2–V4 meet the criterion. These five cases are distinct from the three final-design confirmations above.*

[Case-by-case comparison](data/processed/validation/surrogate/coldplate_validation_comparison.csv) · [Full metric table and interpretation](report/validation/surrogate/README.md) · [Model-selection and split provenance](docs/STUDY_AND_VALIDATION.md)

## Explore the project

| Material | Contents |
|---|---|
| [Final engineering results](results/final_engineering_results/) | Three candidates, original COMSOL exports, plots and workbook |
| [45-case dataset](data/processed/training/SOURCE.md) | Corrected flow/TIM grid, units, split labels and source notes |
| [Study and validation](docs/STUDY_AND_VALIDATION.md) | Model scope, surrogate evaluation, historical mesh study and limitations |
| [Reproduce the reported numbers](docs/portfolio/EVIDENCE_AND_REPRODUCIBILITY.md) | Runnable data checks and source-file manifest |
| [Historical development](docs/history/README.md) | Day 1–3, earlier geometry, mesh/energy records and starter application |

**Scope:** simulation and surrogate-comparison results. Final-geometry energy-balance and mesh-convergence evidence are incomplete in the published package; the exact final GPR checkpoint is not included. These limits are documented in [the technical study](docs/STUDY_AND_VALIDATION.md). Earlier 0.50 × 0.50 mm baseline results are retained as history and are not mixed with the final 0.30 × 0.70 mm study.
