> **Historical project log.** Entries preserve the status and next actions recorded at the time; they are not a current to-do list. The preliminary Day 3 record concerns the 0.50 × 0.50 mm baseline, while the later final study uses 0.30 × 0.70 mm channels. Consult the current overview for the consolidated evidence.
>
> [Current study](README.md) · [History and provenance](docs/history/README.md)

# Project Log

## Daily entry

**Date:**  
**Objective:**  
**Work completed:**  
**Important decisions:**  
**Assumptions:**  
**Problems or risks:**  
**Next action:**  

## 2026-07-29 - Import preliminary Day 3 COMSOL results

**Objective:** Add the baseline and flow-sweep data and figures to the
repository with traceable validation status.

**Work completed:**

- Added three raw COMSOL CSV exports under
  `comsol/exported_results/day03/`.
- Added eleven exported result figures under `figures/day03/`.
- Renamed the misleading `coolant centerline temp.csv` file to
  `channel_centerline_pressure.csv` because the exported expression is
  pressure.
- Documented preliminary thermal and hydraulic trends.

**Important decisions:**

- Preserve the raw numerical contents unchanged.
- Treat the Day 3 dataset as preliminary rather than validated.
- Use readable snake-case filenames in the repository.

**Assumptions:**

- Intended geometry contains ten 0.5 mm x 0.5 mm channels.
- Expected total inlet and outlet area is therefore `2.50e-6 m^2`.

**Problems or risks:**

- The exported outlet area now matches all ten channels.
- Integrated outlet flow is approximately 87.7% of the requested
  flow-rate parameter.
- Results must not be used as the final optimization dataset until the flow
  definition and mass balance are verified.

**Next action:** Verify the COMSOL inlet velocity conversion and boundary
selections, recompute all five flow cases, and confirm mass imbalance below
1% and energy imbalance below 3%.

## 2026-08-06 - Validate surrogate against off-grid COMSOL cases

**Objective:** Compare surrogate predictions with five independent COMSOL
cases and package the results for review.

**Work completed:**

- Added case-level and metric-summary CSV files.
- Added an analysis workbook with a dashboard, source data, and charts.
- Added seven comparison and engineering-interpretation plots.
- Documented validation criteria, results, and scope.

**Important decisions:**

- Keep validation cases within the surrogate's sampled input ranges.
- Use an 85 °C maximum-chip-temperature constraint for classification.
- Report both absolute and percentage errors so small hydraulic errors remain
  interpretable.

**Problems or risks:**

- The validation set contains only five cases, so it is a focused spot check.
- The supplied exports do not contain the full thermal energy-balance terms.
- The conclusions apply to interpolation, not extrapolation beyond training
  bounds.

**Next action:** Expand validation near the 85 °C boundary and include complete
energy-balance exports in the next COMSOL validation batch.
