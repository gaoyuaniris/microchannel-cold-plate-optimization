# Development history and source context

Start with the [current study](../../README.md) for the final design decision and the [evidence index](../portfolio/EVIDENCE_AND_REPRODUCIBILITY.md) for what can be reproduced.

The early baseline used ten **0.50 × 0.50 mm square channels**. The final results package uses ten **0.30 × 0.70 mm rectangular channels**, at 100 W and 25°C inlet. Keep these configurations separate when comparing plots, temperatures, pressure drop and validation claims. Historical files remain in their original locations so source paths and provenance are preserved.

| Record | How to interpret it |
|---|---|
| [Original README at `046d79a`](early_README.md) | Snapshot of the early baseline, preliminary results and roadmap; links rebased for this folder. |
| [Geometry notes](../../comsol/geometry_notes.md), [boundary checklist](../../comsol/boundary_conditions.md), [Day 2 model notes](../../requirements/day02_conjugate_heat_transfer_notes.md) | Initial setup and development notes. Early dimensions and plans are not the final geometry specification. |
| [Early requirements](../../requirements/design_specification.md) and [assumptions](../../requirements/assumptions.md) | Original targets and planning inputs; broader proposed ranges do not imply validated coverage. |
| [Day 3 exports and diagnostic notes](../../comsol/exported_results/day03/README.md), [figure index](../../figures/day03/README.md) | Preliminary square-channel results with a requested-versus-integrated-flow discrepancy. Do not use them as final optimization evidence. |
| [Validation narrative](../model_validation.md) and [mesh/energy report](../../report/validation/mesh_energy_validation.md) | Separate historical square-channel records with different reported mesh temperatures and energy residuals. Their run provenance has not been reconciled; no preferred set of values is asserted here. |
| [Mesh sweep export](../../comsol/exported_results/validation/mesh_sweep_results.csv) and [energy export](../../comsol/exported_results/validation/energy_balance_validation.csv) | Preserve the raw evidence associated with the mesh/energy report. Passing an earlier case does not establish final-geometry verification. |
| [Project log](../../project_log.md) | Dated development status and decisions, not a current task list. |
| [Day 1 learning notes](../../requirements/learning_notes_day1.md), [Day 2 plan](../../requirements/learning_notes_day2.md), [hand calculations](../../hand_calculations/README.md) | Learning material, expectations and first-order square-channel estimates. |
| [Notebook plan](../../notebooks/README.md), [report outline](../../report/report_outline.md), [slide outline](../../presentation/slide_outline.md), [app scaffold](../../app/README.md) | Planning and starter material; their presence does not establish a completed notebook, deck, report or deployed surrogate. |

For the later study, use the [45-case dataset provenance](../../data/processed/training/SOURCE.md), [five off-grid comparisons](../../report/validation/surrogate/README.md) and [three COMSOL-confirmed designs](../../results/final_engineering_results/README.md). Final-geometry mesh and complete energy-balance evidence remain subject to the limits in the [evidence index](../portfolio/EVIDENCE_AND_REPRODUCIBILITY.md).
