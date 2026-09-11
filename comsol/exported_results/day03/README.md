> **Historical preliminary results.** These July 29 exports describe the earlier 0.50 × 0.50 mm square-channel baseline and its unresolved requested-versus-integrated-flow discrepancy. Preserve them as diagnostic history; do not combine their plots or values with the final 0.30 × 0.70 mm study.
>
> [Current study](../../../README.md) · [History and provenance](../../../docs/history/README.md)

# Day 3 COMSOL Results

This directory contains the raw COMSOL 6.3 CSV exports supplied on
July 29, 2026. The associated plots are in `figures/day03/`.

## Included data

- `baseline_summary_results.csv`: baseline maximum chip temperature and
  hotspot coordinates.
- `channel_centerline_pressure.csv`: pressure along a channel centerline.
  The original archive called this file `coolant centerline temp.csv`, but
  its exported expression is pressure, so the file was renamed without
  changing its contents.
- `flow_sweep_summary.csv`: five flow-rate cases from 0.10 to 0.30 L/min
  with temperatures, velocity, thermal resistance, outlet integration,
  pressure drop, and ideal hydraulic pumping power.

## Preliminary trends

Across the requested flow-rate range from 0.10 to 0.30 L/min:

- Maximum chip temperature decreases from about 91.62 to 83.01 degC.
- System thermal resistance decreases from about 0.666 to 0.580 K/W.
- Pressure drop increases from about 1.76 to 7.22 kPa.
- Ideal hydraulic pumping power increases from about 0.00294 to 0.0361 W.

The 0.20 L/min sweep case predicts a maximum chip temperature of about
86.129 degC, consistent with the separate baseline export.

## Validation status

The outlet integration area is `2.50e-6 m^2`, which matches ten
0.5 mm x 0.5 mm channel outlets.

However, the integrated outlet volume flow is approximately 87.7% of the
requested `Vdot_total` in each sweep case. For example:

- Requested flow at the baseline: 0.20 L/min =
  `3.333e-6 m^3/s`
- Integrated outlet flow: `2.919e-6 m^3/s`

The dataset is therefore preliminary. Before using it for optimization,
verify the inlet boundary selection, the conversion from total flow rate to
inlet velocity, and the inlet/outlet flow balance. Then recompute and export
the corrected cases.

## Acceptance gate for the replacement export

- [ ] Ten inlet faces and ten outlet faces are selected.
- [ ] `intopin(1)` and `intopout(1)` both evaluate to about
      `2.50e-6 m^2`.
- [ ] Integrated inlet and outlet volume flow match the requested total
      flow within 1%.
- [ ] Inlet-to-outlet volume-flow imbalance is below 1%.
- [ ] Chip heat and coolant heat-removal imbalance is below 3%.
- [ ] All five flow cases converge on the selected production mesh.
- [ ] Corrected CSV files and figures supersede these preliminary exports.
