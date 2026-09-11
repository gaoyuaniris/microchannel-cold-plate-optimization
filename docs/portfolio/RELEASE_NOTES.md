# Project 1 portfolio consolidation

This portfolio release joins the existing final engineering results with the surrogate-validation records and corrected 45-case dataset. The homepage presents the cooling problem, selected design trade-off and supporting data. Original numerical results and source implementation are preserved.

## Recruiter-facing cleanup — 2026-09-11

- Replaced the preliminary homepage with the final 100 W flow/TIM study, three confirmed candidates, two result figures and direct dataset links.
- Made the 63.5% hydraulic-power comparison explicit: balanced candidate versus minimum-temperature candidate, with a 4.11°C temperature increase.
- Added a technical study record for the dataset, model-selection provenance, five off-grid checks and three confirmation runs.
- Indexed and labeled Day 1–3, the earlier square-channel geometry, learning notes, preliminary mesh reports and starter application as historical material.
- Preserved the earlier README in `docs/history/early_README.md`; `START_HERE.md` now points to the canonical homepage.
- Kept all 17 manifest-listed source files unchanged, including original data, final-result figures and workbooks.

## Provenance

- Common original main: `046d79a255f474d0f0eba67473f217fc80537b19`.
- Branch base, surrogate-validation record: `66e887ef2ccdcbb1b1382e6a045cf4900925c533`.
- Final-engineering-result source: `e2019098164aa8b11c5b8ff5274a6ceedd4b6bfa`.
- All 13 files in `results/final_engineering_results/` are imported using their original Git objects; the existing source branch remains intact.
- The corrected 45-case core CSV and original preparation notes are copied unchanged from the supplied training package. The original raw training export is not republished in this release.

The archived README preserves the original content with relative links rebased for its new location. Historical documents retain their original bodies beneath scope notices; their data and image paths are unchanged. The two earlier mesh narratives report different normal-mesh temperatures and energy residuals, so both are retained as unreconciled historical records rather than final-geometry validation.

## Checks actually performed

For the homepage/history cleanup, the evidence checker again passed **308 checks**, the **eight standard-library portfolio tests** passed, and **115 local Markdown link targets** resolved. All 17 protected source hashes still matched. This documentation cleanup required no new simulations or model fitting.

In an isolated working snapshot, the new standard-library review passed **308 evidence/data checks**: 17 source hashes, complete training grid/split, recorded thermal and hydraulic identities, independently recalculated five-case metrics/classification, and the confirmed trade-off arithmetic.

`python -B -m pytest -p no:cacheprovider tests/ -q` passed **11 tests**: the three inherited tests from the inspected branch plus eight tests for the new review layer. The inherited test files and the two source modules they exercise were verified against their Git blob hashes before execution. This is not a clean installation/retraining test of the entire original project; no COMSOL solve, surrogate training, Pareto search, hardware experiment, or deployed application was run.

New documentation links were checked against the combined repository paths. The source-hash manifest is [source_manifest.json](source_manifest.json); machine-readable recalculated results are [evidence_check_results.json](evidence_check_results.json). Original files are retained even where their source formatting or older terminology differs from the new portfolio notes.

## Evidence limitations

See [evidence and reproducibility](EVIDENCE_AND_REPRODUCIBILITY.md), especially missing final-geometry mesh/energy-balance evidence and final GPR checkpoint/pipeline provenance. The nine-row model-selection holdout and five off-grid comparison records serve different purposes. The final package TIM values are metadata, and hydraulic pumping power excludes electrical pump efficiency and external loop losses. The portfolio reports a simulation study; it does not claim measured hardware performance.
