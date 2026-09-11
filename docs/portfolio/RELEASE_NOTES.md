# Project 1 portfolio consolidation

This review branch joins the existing final engineering results with the existing surrogate-validation records and adds a job-search navigation/review layer. It does not change the COMSOL results, model coefficients, training predictions, existing source implementation, or repository visibility.

## Provenance

- Common original main: `046d79a255f474d0f0eba67473f217fc80537b19`.
- Branch base, surrogate-validation record: `66e887ef2ccdcbb1b1382e6a045cf4900925c533`.
- Final-engineering-result source: `e2019098164aa8b11c5b8ff5274a6ceedd4b6bfa`.
- All 13 files in `results/final_engineering_results/` are imported using their original Git objects; the existing source branch remains intact.
- The corrected 45-case core CSV and original preparation notes are copied unchanged from the supplied training package. The original raw training export is not republished in this release.

The root README retains the complete pre-existing body with a short portfolio navigation notice prepended. No historical baseline file is moved or relabeled as final-geometry evidence. Existing code, plots, validation tables and workbooks are preserved.

## Checks actually performed

In an isolated working snapshot, the new standard-library review passed **308 evidence/data checks**: 17 source hashes, complete training grid/split, recorded thermal and hydraulic identities, independently recalculated five-case metrics/classification, and the confirmed trade-off arithmetic.

`python -B -m pytest -p no:cacheprovider tests/ -q` passed **11 tests**: the three inherited tests from the inspected branch plus eight tests for the new review layer. The inherited test files and the two source modules they exercise were verified against their Git blob hashes before execution. This is not a clean installation/retraining test of the entire original project; no COMSOL solve, surrogate training, Pareto search, hardware experiment, or deployed application was run.

New documentation links were checked against the combined repository paths. The source-hash manifest is [source_manifest.json](source_manifest.json); machine-readable recalculated results are [evidence_check_results.json](evidence_check_results.json). Original files are retained even where their source formatting or older terminology differs from the new portfolio notes.

## Remaining items before wider release

Review [evidence and reproducibility](EVIDENCE_AND_REPRODUCIBILITY.md), especially missing final-geometry energy-balance fields and final GPR checkpoint/pipeline provenance. The nine-row development holdout and five independent comparison records must not be conflated. The final package TIM values are metadata, and hydraulic pumping power is not electrical pump consumption.

The repository is private. This change is proposed through a separate branch/pull request, without a main-branch merge, force-push, visibility change, license change, or editing of the user's local project folder. Public recruiter access requires a deliberate owner decision and review of the full repository/history, not just this added documentation.
