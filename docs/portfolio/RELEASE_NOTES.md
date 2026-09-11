# Project 1 portfolio consolidation

This portfolio release joins the final engineering results with the surrogate-validation records and corrected 45-case dataset. The homepage presents the cooling problem, selected design trade-off and supporting data. All 17 manifest-listed evidence files are preserved unchanged.

## Recruiter-facing cleanup — 2026-09-11

- Replaced the preliminary homepage with the final 100 W flow/TIM study, three confirmed candidates, two result figures and direct dataset links.
- Made the 63.5% hydraulic-power comparison explicit: balanced candidate versus minimum-temperature candidate, with a 4.11°C temperature increase.
- Added a technical study record for the dataset, model-selection provenance, five off-grid checks and three confirmation runs.
- Removed Day 1–3 learning notes, preliminary exports/figures, old setup checklists, development plans, baseline hand calculations, the duplicated old homepage and the placeholder application from the current version.
- Removed the development-history navigation; `START_HERE.md` points to the canonical homepage and supporting technical documents.
- Retained the earlier-baseline mesh/energy evidence with explicit configuration and provenance limits in the technical study.
- Kept all 17 manifest-listed source files unchanged, including original data, final-result figures and workbooks.

## Provenance

- Common original main: `046d79a255f474d0f0eba67473f217fc80537b19`.
- Branch base, surrogate-validation record: `66e887ef2ccdcbb1b1382e6a045cf4900925c533`.
- Final-engineering-result source: `e2019098164aa8b11c5b8ff5274a6ceedd4b6bfa`.
- All 13 files in `results/final_engineering_results/` are imported using their original Git objects; the existing source branch remains intact.
- The corrected 45-case core CSV and original preparation notes are copied unchanged from the supplied training package. The original raw training export is not republished in this release.

Removed development material remains recoverable in Git history at commit `882817ea66c738544dbaa0c49e9bd935f45409be`. It is no longer part of the current portfolio navigation or file tree. The two retained mesh narratives report different normal-mesh temperatures and energy residuals, so neither is presented as final-geometry validation.

## Checks actually performed

The evidence checker passed **308 checks** covering the 17 source hashes, complete training grid/split, thermal and hydraulic identities, five-case metrics/classification and confirmed trade-off arithmetic. The **eight standard-library portfolio tests** also passed. The remaining Markdown links were checked after removing the development files.

The source-hash manifest is [source_manifest.json](source_manifest.json); machine-readable recalculated results are [evidence_check_results.json](evidence_check_results.json). No COMSOL solve, surrogate fitting, Pareto search or hardware test was performed during this presentation cleanup.

## Evidence limitations

See [evidence and reproducibility](EVIDENCE_AND_REPRODUCIBILITY.md), especially missing final-geometry mesh/energy-balance evidence and final GPR checkpoint/pipeline provenance. The nine-row model-selection holdout and five off-grid comparison records serve different purposes. The final package TIM values are metadata, and hydraulic pumping power excludes electrical pump efficiency and external loop losses. The portfolio reports a simulation study; it does not claim measured hardware performance.
