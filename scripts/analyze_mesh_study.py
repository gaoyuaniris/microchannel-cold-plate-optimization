#!/usr/bin/env python3
"""Process COMSOL mesh-sweep and integrated energy-balance CSV exports.

This script reads the raw multi-block CSV layout produced by COMSOL, creates
tidy processed tables, applies the project's validation thresholds, generates
plots, and writes a Markdown validation report. It never invents simulation
data: missing required values stop the analysis with a clear error.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


MESH_ORDER = ["coarse", "normal", "fine", "finer", "extreme fine"]
REFERENCE_PRIORITY = ["extreme fine", "finer", "fine", "normal", "coarse"]

CONVERGENCE_RULES = {
    "max_chip_temperature_C": ("absolute", 0.5, "°C"),
    "thermal_resistance_K_W": ("percent", 1.0, "%"),
    "pressure_drop_Pa": ("percent", 3.0, "%"),
    "pumping_power_W": ("percent", 3.0, "%"),
    "outlet_temperature_C": ("absolute", 0.2, "°C"),
}

FLOW_IMBALANCE_LIMIT_PCT = 0.5
ENERGY_BALANCE_LIMIT_PCT = 2.0

MESH_OUTPUT_COLUMNS = [
    "mesh_level",
    "flow_rate_L_min",
    "max_chip_temperature_C",
    "thermal_resistance_K_W",
    "pressure_drop_Pa",
    "pumping_power_W",
    "outlet_temperature_C",
    "outlet_flow_m3_s",
    "inlet_flow_m3_s",
    "flow_imbalance_pct",
]

ENERGY_OUTPUT_COLUMNS = [
    "validation_mesh",
    "flow_rate_L_min",
    "total_heat_source_W",
    "heat_balance_residual_W",
    "energy_balance_residual_W",
    "heat_balance_error_pct",
    "energy_balance_error_pct",
    "heat_balance_passes",
    "energy_balance_passes",
]

METRIC_OUTPUT_COLUMNS = [
    "flow_rate_L_min",
    "comparison",
    "candidate_mesh",
    "reference_mesh",
    "metric",
    "candidate_value",
    "reference_value",
    "difference",
    "difference_type",
    "limit",
    "unit",
    "passes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze COMSOL cold-plate mesh and energy validation exports."
    )
    parser.add_argument(
        "--mesh-input",
        type=Path,
        default=Path(
            "comsol/exported_results/validation/mesh_sweep_results.csv"
        ),
        help="Raw COMSOL mesh-sweep CSV.",
    )
    parser.add_argument(
        "--energy-input",
        type=Path,
        default=Path(
            "comsol/exported_results/validation/energy_balance_validation.csv"
        ),
        help="Raw COMSOL global energy-balance CSV.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed/validation"),
        help="Directory for normalized and calculated CSVs.",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("figures/validation"),
        help="Directory for validation plots.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("report/validation/mesh_energy_validation.md"),
        help="Generated Markdown validation report.",
    )
    parser.add_argument(
        "--design-flow-l-min",
        type=float,
        default=0.25,
        help="Design flow rate used for the recommendation (default: 0.25).",
    )
    parser.add_argument(
        "--energy-mesh",
        default="normal",
        help="Mesh used for the energy-balance export (default: normal).",
    )
    return parser.parse_args()


def normalize_text(value: object) -> str:
    return " ".join(str(value).strip().lower().replace("weitghted", "weighted").split())


def read_comsol_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise ValueError(f"Required COMSOL export was not found: {path}")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
    except csv.Error as exc:
        raise ValueError(f"Could not parse COMSOL CSV {path}: {exc}") from exc
    if not rows:
        raise ValueError(f"COMSOL export contains no rows: {path}")
    width = max(len(row) for row in rows)
    padded_rows = [row + [""] * (width - len(row)) for row in rows]
    return pd.DataFrame(padded_rows, dtype=str)


def find_column(headers: list[str], description: str, predicate) -> int:
    matches = [index for index, header in enumerate(headers) if predicate(header)]
    if len(matches) != 1:
        raise ValueError(
            f"Expected one {description} column, found {len(matches)}. "
            "Check that the COMSOL table expressions have not changed."
        )
    return matches[0]


def to_number(value: object, context: str) -> float:
    try:
        number = float(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"Missing or non-numeric value for {context}: {value!r}") from exc
    if not math.isfinite(number):
        raise ValueError(f"Non-finite value for {context}: {value!r}")
    return number


def parse_mesh_sweep(path: Path) -> pd.DataFrame:
    raw = read_comsol_csv(path)
    records: list[dict[str, float | str]] = []
    row_index = 0

    while row_index < len(raw):
        first_cell = normalize_text(raw.iat[row_index, 0])
        if first_cell not in MESH_ORDER:
            row_index += 1
            continue

        mesh_level = first_cell
        header_index = row_index + 1
        if header_index >= len(raw):
            raise ValueError(f"Missing header row after mesh label {mesh_level!r}.")
        headers = [normalize_text(value) for value in raw.iloc[header_index].tolist()]

        flow_col = find_column(
            headers, "flow-rate", lambda value: "vdot_total" in value
        )
        rth_col = find_column(
            headers,
            "thermal-resistance",
            lambda value: "system thermal resistance" in value,
        )
        outlet_temp_col = find_column(
            headers,
            "mass-weighted outlet-temperature",
            lambda value: "mass weighted" in value,
        )
        pumping_col = find_column(
            headers, "pumping-power", lambda value: "pumping power" in value
        )
        pressure_col = find_column(
            headers, "pressure-drop", lambda value: "pressure drop" in value
        )
        outlet_flow_col = find_column(
            headers,
            "outlet volume-flow",
            lambda value: value.startswith("outlet integration") and "m^3/s" in value,
        )
        inlet_flow_col = find_column(
            headers, "inlet volume-flow", lambda value: value.startswith("qin")
        )

        # COMSOL's first Temperature column in this table is the maximum chip value.
        temperature_columns = [
            index for index, header in enumerate(headers) if header == "temperature (degc)"
        ]
        if not temperature_columns:
            raise ValueError(f"No temperature column found for mesh {mesh_level!r}.")
        tmax_col = temperature_columns[0]

        data_index = header_index + 1
        mesh_row_count = 0
        while data_index < len(raw):
            first_value = normalize_text(raw.iat[data_index, 0])
            if not first_value or first_value in MESH_ORDER or first_value.startswith("%"):
                break
            try:
                flow_rate = float(first_value)
            except ValueError:
                break

            q_out = to_number(
                raw.iat[data_index, outlet_flow_col],
                f"{mesh_level} outlet flow at {flow_rate:g} L/min",
            )
            q_in = to_number(
                raw.iat[data_index, inlet_flow_col],
                f"{mesh_level} inlet flow at {flow_rate:g} L/min",
            )
            if q_in <= 0 or q_out <= 0:
                raise ValueError("Inlet and outlet flow magnitudes must be positive.")

            records.append(
                {
                    "mesh_level": mesh_level,
                    "flow_rate_L_min": flow_rate,
                    "max_chip_temperature_C": to_number(
                        raw.iat[data_index, tmax_col], "maximum chip temperature"
                    ),
                    "thermal_resistance_K_W": to_number(
                        raw.iat[data_index, rth_col], "thermal resistance"
                    ),
                    "pressure_drop_Pa": to_number(
                        raw.iat[data_index, pressure_col], "pressure drop"
                    ),
                    "pumping_power_W": to_number(
                        raw.iat[data_index, pumping_col], "pumping power"
                    ),
                    "outlet_temperature_C": to_number(
                        raw.iat[data_index, outlet_temp_col],
                        "mass-weighted outlet temperature",
                    ),
                    "outlet_flow_m3_s": q_out,
                    "inlet_flow_m3_s": q_in,
                    "flow_imbalance_pct": abs(q_out - q_in) / abs(q_in) * 100.0,
                }
            )
            mesh_row_count += 1
            data_index += 1

        if mesh_row_count == 0:
            raise ValueError(f"No numerical rows found for mesh {mesh_level!r}.")
        row_index = data_index

    if not records:
        raise ValueError("No coarse, normal, fine, finer, or extreme-fine blocks found.")

    result = pd.DataFrame.from_records(records, columns=MESH_OUTPUT_COLUMNS)
    if result.duplicated(["mesh_level", "flow_rate_L_min"]).any():
        raise ValueError("Duplicate mesh/flow combinations were found in the mesh export.")
    mesh_rank = {mesh: index for index, mesh in enumerate(MESH_ORDER)}
    result["_mesh_rank"] = result["mesh_level"].map(mesh_rank)
    return (
        result.sort_values(["flow_rate_L_min", "_mesh_rank"])
        .drop(columns="_mesh_rank")
        .reset_index(drop=True)
    )


def parse_energy_balance(path: Path, validation_mesh: str) -> pd.DataFrame:
    raw = read_comsol_csv(path)
    header_index = None
    for index in range(len(raw)):
        row_text = [normalize_text(value) for value in raw.iloc[index].tolist()]
        if any("total heat source" in value for value in row_text) and any(
            "energy balance" in value for value in row_text
        ):
            header_index = index
            headers = row_text
            break
    if header_index is None:
        raise ValueError("Could not find the energy-balance header row.")

    flow_col = find_column(headers, "flow-rate", lambda value: "vdot_total" in value)
    source_col = find_column(
        headers, "total heat source", lambda value: "total heat source" in value
    )
    heat_col = find_column(
        headers,
        "heat-balance residual",
        lambda value: value.startswith("heat balance") and "error" not in value,
    )
    energy_col = find_column(
        headers,
        "energy-balance residual",
        lambda value: value.startswith("energy balance") and "error" not in value,
    )

    records = []
    for index in range(header_index + 1, len(raw)):
        first_value = normalize_text(raw.iat[index, flow_col])
        if not first_value:
            continue
        try:
            flow_rate = float(first_value)
        except ValueError:
            continue
        heat_source = to_number(raw.iat[index, source_col], "total heat source")
        heat_residual = to_number(raw.iat[index, heat_col], "heat-balance residual")
        energy_residual = to_number(
            raw.iat[index, energy_col], "energy-balance residual"
        )
        if heat_source == 0:
            raise ValueError("Total heat source cannot be zero for percentage errors.")
        heat_error = abs(heat_residual) / abs(heat_source) * 100.0
        energy_error = abs(energy_residual) / abs(heat_source) * 100.0
        records.append(
            {
                "validation_mesh": normalize_text(validation_mesh),
                "flow_rate_L_min": flow_rate,
                "total_heat_source_W": heat_source,
                "heat_balance_residual_W": heat_residual,
                "energy_balance_residual_W": energy_residual,
                "heat_balance_error_pct": heat_error,
                "energy_balance_error_pct": energy_error,
                "heat_balance_passes": heat_error < ENERGY_BALANCE_LIMIT_PCT,
                "energy_balance_passes": energy_error < ENERGY_BALANCE_LIMIT_PCT,
            }
        )

    if not records:
        raise ValueError("No numerical rows found in the energy-balance export.")
    return pd.DataFrame.from_records(records, columns=ENERGY_OUTPUT_COLUMNS).sort_values(
        "flow_rate_L_min"
    )


def select_reference_mesh(mesh_results: pd.DataFrame) -> str:
    available = set(mesh_results["mesh_level"])
    for mesh in REFERENCE_PRIORITY:
        if mesh in available:
            return mesh
    raise ValueError("No supported reference mesh was found.")


def percent_difference(candidate: float, reference: float, metric: str) -> float:
    if reference == 0:
        raise ValueError(f"Cannot calculate {metric} percent difference from zero.")
    return abs(candidate - reference) / abs(reference) * 100.0


def calculate_convergence_metrics(
    mesh_results: pd.DataFrame, reference_mesh: str
) -> pd.DataFrame:
    records = []
    reference_rows = mesh_results[mesh_results["mesh_level"] == reference_mesh].set_index(
        "flow_rate_L_min"
    )
    candidates = [
        mesh for mesh in MESH_ORDER if mesh in set(mesh_results["mesh_level"]) and mesh != reference_mesh
    ]

    for candidate_mesh in candidates:
        candidate_rows = mesh_results[
            mesh_results["mesh_level"] == candidate_mesh
        ].set_index("flow_rate_L_min")
        common_flows = sorted(set(candidate_rows.index) & set(reference_rows.index))
        if not common_flows:
            raise ValueError(f"No common flow rates for {candidate_mesh} and {reference_mesh}.")
        for flow_rate in common_flows:
            for metric, (difference_type, limit, unit) in CONVERGENCE_RULES.items():
                candidate = float(candidate_rows.loc[flow_rate, metric])
                reference = float(reference_rows.loc[flow_rate, metric])
                difference = (
                    abs(candidate - reference)
                    if difference_type == "absolute"
                    else percent_difference(candidate, reference, metric)
                )
                records.append(
                    {
                        "flow_rate_L_min": flow_rate,
                        "comparison": f"{candidate_mesh}-to-{reference_mesh}",
                        "candidate_mesh": candidate_mesh,
                        "reference_mesh": reference_mesh,
                        "metric": metric,
                        "candidate_value": candidate,
                        "reference_value": reference,
                        "difference": difference,
                        "difference_type": difference_type,
                        "limit": limit,
                        "unit": unit,
                        "passes": difference < limit,
                    }
                )

    return pd.DataFrame.from_records(records, columns=METRIC_OUTPUT_COLUMNS)


def value_at_flow(frame: pd.DataFrame, flow: float, label: str) -> pd.DataFrame:
    selection = frame[(frame["flow_rate_L_min"] - flow).abs() < 1.0e-10]
    if selection.empty:
        available = ", ".join(f"{value:g}" for value in sorted(frame["flow_rate_L_min"].unique()))
        raise ValueError(f"No {label} row at {flow:g} L/min. Available: {available}")
    return selection


def build_design_summary(
    mesh_results: pd.DataFrame,
    energy_results: pd.DataFrame,
    design_flow: float,
) -> pd.DataFrame:
    design = value_at_flow(mesh_results, design_flow, "mesh").copy()
    energy = value_at_flow(energy_results, design_flow, "energy-balance")
    validation_mesh = str(energy.iloc[0]["validation_mesh"])
    design["energy_balance_error_pct"] = math.nan
    design["energy_balance_passes"] = pd.NA
    target = design["mesh_level"] == validation_mesh
    if not target.any():
        raise ValueError(
            f"Energy validation mesh {validation_mesh!r} is not present in the mesh sweep."
        )
    design.loc[target, "energy_balance_error_pct"] = float(
        energy.iloc[0]["energy_balance_error_pct"]
    )
    design.loc[target, "energy_balance_passes"] = bool(
        energy.iloc[0]["energy_balance_passes"]
    )
    design["flow_imbalance_passes"] = (
        design["flow_imbalance_pct"] < FLOW_IMBALANCE_LIMIT_PCT
    )
    return design


def make_decision(
    metrics: pd.DataFrame,
    design_summary: pd.DataFrame,
    energy_results: pd.DataFrame,
    reference_mesh: str,
    design_flow: float,
    preferred_mesh: str = "normal",
) -> pd.DataFrame:
    design_metrics = value_at_flow(metrics, design_flow, "convergence")
    candidate_metrics = design_metrics[
        design_metrics["candidate_mesh"] == preferred_mesh
    ]
    if candidate_metrics.empty:
        raise ValueError(f"Preferred mesh {preferred_mesh!r} is not available for comparison.")

    candidate_summary = design_summary[
        design_summary["mesh_level"] == preferred_mesh
    ]
    if candidate_summary.empty:
        raise ValueError(f"No design-point summary for mesh {preferred_mesh!r}.")
    energy_at_design = value_at_flow(energy_results, design_flow, "energy-balance")

    convergence_passes = bool(candidate_metrics["passes"].all())
    flow_passes = bool(candidate_summary.iloc[0]["flow_imbalance_passes"])
    energy_passes = bool(energy_at_design.iloc[0]["energy_balance_passes"])
    all_pass = convergence_passes and flow_passes and energy_passes
    recommendation = preferred_mesh if all_pass else "no recommendation"
    status = "PASS" if all_pass else "REVIEW"

    return pd.DataFrame(
        [
            {
                "design_flow_L_min": design_flow,
                "candidate_mesh": preferred_mesh,
                "reference_mesh": reference_mesh,
                "convergence_passes": convergence_passes,
                "flow_imbalance_passes": flow_passes,
                "energy_balance_passes": energy_passes,
                "overall_status": status,
                "recommended_mesh": recommendation,
            }
        ]
    )


def style_axis(axis: plt.Axes) -> None:
    axis.grid(True, alpha=0.25)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def plot_mesh_metric(
    mesh_results: pd.DataFrame,
    column: str,
    ylabel: str,
    title: str,
    path: Path,
) -> None:
    figure, axis = plt.subplots(figsize=(7.2, 4.8))
    for mesh in MESH_ORDER:
        rows = mesh_results[mesh_results["mesh_level"] == mesh].sort_values(
            "flow_rate_L_min"
        )
        if rows.empty:
            continue
        axis.plot(
            rows["flow_rate_L_min"],
            rows[column],
            marker="o",
            linewidth=2,
            label=mesh.title(),
        )
    axis.set_title(title)
    axis.set_xlabel("Total flow rate (L/min)")
    axis.set_ylabel(ylabel)
    style_axis(axis)
    axis.legend()
    figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def plot_energy_errors(energy: pd.DataFrame, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(7.2, 4.8))
    axis.plot(
        energy["flow_rate_L_min"],
        energy["heat_balance_error_pct"],
        marker="o",
        linewidth=2,
        label="Heat-balance error",
    )
    axis.plot(
        energy["flow_rate_L_min"],
        energy["energy_balance_error_pct"],
        marker="s",
        linewidth=2,
        label="Energy-balance error",
    )
    axis.axhline(
        ENERGY_BALANCE_LIMIT_PCT,
        color="#c62828",
        linestyle="--",
        linewidth=1.8,
        label="2% acceptance limit",
    )
    axis.set_title("COMSOL-integrated balance errors")
    axis.set_xlabel("Total flow rate (L/min)")
    axis.set_ylabel("Absolute error (%)")
    axis.set_ylim(bottom=0)
    style_axis(axis)
    axis.legend()
    figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def format_markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    formatted = frame[columns].copy()
    for column in formatted.columns:
        if pd.api.types.is_float_dtype(formatted[column]):
            formatted[column] = formatted[column].map(lambda value: f"{value:.4f}")
    header = "| " + " | ".join(formatted.columns) + " |"
    separator = "|" + "|".join("---" for _ in formatted.columns) + "|"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in formatted.itertuples(index=False, name=None)
    ]
    return "\n".join([header, separator, *rows])


def write_report(
    path: Path,
    decision: pd.DataFrame,
    design_summary: pd.DataFrame,
    metrics: pd.DataFrame,
    energy: pd.DataFrame,
    design_flow: float,
    mesh_source: Path,
    energy_source: Path,
) -> None:
    row = decision.iloc[0]
    candidate = str(row["candidate_mesh"])
    reference = str(row["reference_mesh"])
    design_metrics = value_at_flow(metrics, design_flow, "convergence")
    design_metrics = design_metrics[design_metrics["candidate_mesh"] == candidate]
    design_energy = value_at_flow(energy, design_flow, "energy-balance")

    metric_table = design_metrics[
        ["metric", "difference", "limit", "unit", "passes"]
    ].rename(
        columns={
            "metric": "Metric",
            "difference": "Difference",
            "limit": "Limit",
            "unit": "Unit",
            "passes": "Pass",
        }
    )
    energy_table = energy[
        [
            "flow_rate_L_min",
            "total_heat_source_W",
            "heat_balance_error_pct",
            "energy_balance_error_pct",
            "energy_balance_passes",
        ]
    ].rename(
        columns={
            "flow_rate_L_min": "Flow (L/min)",
            "total_heat_source_W": "Heat source (W)",
            "heat_balance_error_pct": "Heat error (%)",
            "energy_balance_error_pct": "Energy error (%)",
            "energy_balance_passes": "Pass",
        }
    )
    summary_table = design_summary[
        [
            "mesh_level",
            "max_chip_temperature_C",
            "thermal_resistance_K_W",
            "pressure_drop_Pa",
            "pumping_power_W",
            "outlet_temperature_C",
            "flow_imbalance_pct",
        ]
    ].rename(
        columns={
            "mesh_level": "Mesh",
            "max_chip_temperature_C": "Tmax (°C)",
            "thermal_resistance_K_W": "Rth (K/W)",
            "pressure_drop_Pa": "Pressure drop (Pa)",
            "pumping_power_W": "Pumping power (W)",
            "outlet_temperature_C": "Outlet T (°C)",
            "flow_imbalance_pct": "Flow imbalance (%)",
        }
    )

    report = f"""# Mesh and energy validation

## Conclusion

**Overall status: {row['overall_status']}**

At {design_flow:g} L/min, the **{candidate} mesh** passes all convergence,
flow-conservation, and COMSOL-integrated energy-balance criteria relative to
the **{reference} mesh**. Recommended production mesh: **{row['recommended_mesh']}**.

## Design-point results

{format_markdown_table(summary_table, list(summary_table.columns))}

## {candidate.title()}-to-{reference.title()} convergence checks

{format_markdown_table(metric_table, list(metric_table.columns))}

## COMSOL-integrated balance checks

{format_markdown_table(energy_table, list(energy_table.columns))}

At the design point, the integrated energy-balance error is
{float(design_energy.iloc[0]['energy_balance_error_pct']):.4f}%, below the
{ENERGY_BALANCE_LIMIT_PCT:g}% acceptance limit.

## Acceptance criteria

- Tmax absolute difference < 0.5 °C
- Thermal-resistance difference < 1%
- Pressure-drop difference < 3%
- Pumping-power difference < 3%
- Outlet-temperature absolute difference < 0.2 °C
- Flow imbalance < 0.5%
- COMSOL-integrated energy-balance error < 2%

## Reproduce

```bash
python3 scripts/analyze_mesh_study.py
```

Raw sources:

- `{mesh_source.as_posix()}`
- `{energy_source.as_posix()}`

Element counts and solve times were not present in the supplied COMSOL exports,
so they are not reported or estimated.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        if not math.isfinite(args.design_flow_l_min) or args.design_flow_l_min <= 0:
            raise ValueError("--design-flow-l-min must be finite and greater than zero.")

        mesh_results = parse_mesh_sweep(args.mesh_input)
        energy_results = parse_energy_balance(args.energy_input, args.energy_mesh)
        reference_mesh = select_reference_mesh(mesh_results)
        metrics = calculate_convergence_metrics(mesh_results, reference_mesh)
        design_summary = build_design_summary(
            mesh_results, energy_results, args.design_flow_l_min
        )
        decision = make_decision(
            metrics,
            design_summary,
            energy_results,
            reference_mesh,
            args.design_flow_l_min,
        )

        args.processed_dir.mkdir(parents=True, exist_ok=True)
        args.figures_dir.mkdir(parents=True, exist_ok=True)
        mesh_results.to_csv(args.processed_dir / "mesh_results_tidy.csv", index=False)
        metrics.to_csv(args.processed_dir / "convergence_metrics.csv", index=False)
        energy_results.to_csv(
            args.processed_dir / "energy_balance_summary.csv", index=False
        )
        design_summary.to_csv(
            args.processed_dir / "design_point_summary.csv", index=False
        )
        decision.to_csv(args.processed_dir / "validation_decision.csv", index=False)

        plot_mesh_metric(
            mesh_results,
            "max_chip_temperature_C",
            "Maximum chip temperature (°C)",
            "Maximum chip temperature vs flow rate",
            args.figures_dir / "tmax_vs_flow_rate.png",
        )
        plot_mesh_metric(
            mesh_results,
            "pressure_drop_Pa",
            "Pressure drop (Pa)",
            "Pressure drop vs flow rate",
            args.figures_dir / "pressure_drop_vs_flow_rate.png",
        )
        plot_mesh_metric(
            mesh_results,
            "pumping_power_W",
            "Pumping power (W)",
            "Pumping power vs flow rate",
            args.figures_dir / "pumping_power_vs_flow_rate.png",
        )
        plot_energy_errors(
            energy_results, args.figures_dir / "energy_balance_error_vs_flow_rate.png"
        )
        write_report(
            args.report,
            decision,
            design_summary,
            metrics,
            energy_results,
            args.design_flow_l_min,
            args.mesh_input,
            args.energy_input,
        )

        result = decision.iloc[0]
        print(f"Validation status: {result['overall_status']}")
        print(f"Recommended mesh: {result['recommended_mesh']}")
        print(f"Reference mesh: {reference_mesh}")
        print(f"Processed tables: {args.processed_dir}")
        print(f"Figures: {args.figures_dir}")
        print(f"Report: {args.report}")
        return 0
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
