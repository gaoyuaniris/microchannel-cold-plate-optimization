"""Recalculate Project 1's recorded evidence, not its original CFD/GPR fits.

Standard-library only. Run: python scripts/review_project1.py
Use --json-out PATH to write the checked summary without modifying source data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAINING = "data/processed/training/coldplate_ml_core_45.csv"
VALIDATION = "data/processed/validation/surrogate/coldplate_validation_comparison.csv"
METRICS = "data/processed/validation/surrogate/coldplate_validation_metrics_summary.csv"
CONFIRMED = "results/final_engineering_results/data/final_selected_designs_comsol_confirmed.csv"


def read_rows(root: Path, path: str) -> list[dict[str, str]]:
    with (root / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def error_metrics(actual: list[float], predicted: list[float]) -> dict[str, float]:
    """Compute recorded-output comparison metrics, with nonzero references."""
    if not actual or len(actual) != len(predicted):
        raise ValueError("Expected equal, nonempty reference and prediction lists.")
    if not all(math.isfinite(v) for v in actual + predicted):
        raise ValueError("Values must be finite.")
    if any(v == 0 for v in actual):
        raise ValueError("Percentage errors require nonzero reference values.")
    errors = [p - a for a, p in zip(actual, predicted)]
    n = len(errors)
    mean = sum(actual) / n
    ss_total = sum((a - mean) ** 2 for a in actual)
    return {
        "MAE": sum(abs(e) for e in errors) / n,
        "RMSE": math.sqrt(sum(e * e for e in errors) / n),
        "MAPE_percent": 100 * sum(abs(e / a) for e, a in zip(errors, actual)) / n,
        "Max_absolute_error": max(abs(e) for e in errors),
        "R2": 1 - sum(e * e for e in errors) / ss_total if ss_total else float("nan"),
    }


def review_project(root: Path = ROOT) -> dict:
    """Raise AssertionError for evidence inconsistencies; return checked results."""
    checks = 0

    def require(ok: bool, message: str) -> None:
        nonlocal checks
        if not ok:
            raise AssertionError(message)
        checks += 1

    manifest = json.loads((root / "docs/portfolio/source_manifest.json").read_text())
    for record in manifest["source_files"]:
        content = (root / record["path"]).read_bytes()
        actual_hash = hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()
        require(actual_hash == record["git_blob_sha"], f"Source changed: {record['path']}")

    training = read_rows(root, TRAINING)
    expected_grid = set(itertools.product([.10, .15, .20, .25, .30], [.05, .10, .15], [1.5, 3., 6.]))
    keys = [(float(r["flow_rate_Lmin"]), float(r["TIM_thickness_mm"]), float(r["TIM_conductivity_W_mK"])) for r in training]
    require(len(training) == 45 and len(set(keys)) == 45, "Expected 45 unique training-grid rows.")
    require(set(keys) == expected_grid, "Incomplete or different flow/TIM grid.")
    split_counts = {s: sum(r["dataset_split"] == s for r in training) for s in ["train_cv", "test_holdout"]}
    require(split_counts == {"train_cv": 36, "test_holdout": 9}, "Unexpected supplied split labels.")
    for row in training:
        q = float(row["flow_rate_Lmin"])
        t = float(row["Tmax_chip_C"])
        require((row["dataset_split"] == "test_holdout") == (q == .25), "Holdout flow changed.")
        require(math.isclose((t - 25) / 100, float(row["system_thermal_resistance_K_W"]), abs_tol=1e-12), "Training Rth identity.")
        require(math.isclose(float(row["pressure_drop_Pa"]) * q / 60000, float(row["pumping_power_W"]), rel_tol=1e-9), "Training hydraulic-power identity.")
        require(int(row["thermal_limit_pass"]) == int(t <= 85), "Training thermal classification.")
        require(row["energy_balance_available"] == "0", "Energy evidence changed; update scope documentation.")
    feasible = sum(float(r["Tmax_chip_C"]) <= 85 for r in training)
    require(feasible == 19, "Unexpected count of thermally feasible grid points.")

    validation = read_rows(root, VALIDATION)
    require({r["case_id"] for r in validation} == {"V1", "V2", "V3", "V4", "V5"}, "Five-case evidence IDs differ.")
    require(len(validation) == 5, "Expected five independent comparison rows.")
    for row in validation:
        require(.10 <= float(row["flow_rate_set_Lmin"]) <= .30, "Off-grid case outside flow domain.")
        require(.05 <= float(row["TIM_thickness_mm"]) <= .15, "Off-grid case outside thickness domain.")
        require(1.5 <= float(row["TIM_conductivity_W_mK"]) <= 6, "Off-grid case outside conductivity domain.")
        require((float(row["predicted_Tmax_C"]) <= 85) == (float(row["COMSOL_Tmax_C"]) <= 85), "Prediction/CFD classification differs.")

    targets = {
        "Maximum chip temperature": ("COMSOL_Tmax_C", "predicted_Tmax_C"),
        "System thermal resistance": ("COMSOL_system_Rth_K_W", "predicted_system_Rth_K_W"),
        "Mass-weighted outlet temperature": ("COMSOL_Tout_C", "predicted_Tout_C"),
        "Pressure drop": ("COMSOL_pressure_drop_Pa", "predicted_pressure_drop_Pa"),
        "Pumping power": ("COMSOL_pump_power_W", "predicted_pump_power_W"),
    }
    saved = {r["parameter"]: r for r in read_rows(root, METRICS)}
    computed = {}
    for name, (actual_key, predicted_key) in targets.items():
        values = error_metrics([float(r[actual_key]) for r in validation], [float(r[predicted_key]) for r in validation])
        for metric, value in values.items():
            require(math.isclose(value, float(saved[name][metric]), rel_tol=1e-9, abs_tol=1e-12), f"Mismatch: {name} {metric}")
        computed[name] = values

    confirmed = read_rows(root, CONFIRMED)
    require(len(confirmed) == 3, "Expected three final confirmation cases.")
    by_name = {r["design"]: r for r in confirmed}
    for row in confirmed:
        t = float(row["Tmax_C"])
        require(math.isclose(85 - t, float(row["thermal_margin_to_85C_C"]), abs_tol=1e-10), "Confirmation thermal margin.")
        require(math.isclose((t - 25) / 100, float(row["system_Rth_K_W"]), abs_tol=1e-12), "Confirmation Rth identity.")
        require(math.isclose(float(row["pressure_drop_Pa"]) * float(row["flow_rate_Lmin"]) / 60000, float(row["pumping_power_W"]), rel_tol=2e-6), "Confirmation hydraulic-power identity.")
        require(t <= 85 and row["thermal_limit_status"] == "PASS", "Confirmation thermal criterion.")
    knee, minimum_t = by_name["Balanced knee point"], by_name["Minimum temperature"]
    saving = 100 * (1 - float(knee["pumping_power_W"]) / float(minimum_t["pumping_power_W"]))
    penalty = float(knee["Tmax_C"]) - float(minimum_t["Tmax_C"])
    require(math.isclose(saving, 63.53378222871247, abs_tol=1e-10), "Balanced-design pumping comparison.")
    require(math.isclose(penalty, 4.1069606687350415, abs_tol=1e-10), "Balanced-design temperature comparison.")
    return {
        "checks_passed": checks,
        "grid_rows": 45,
        "split_counts": split_counts,
        "thermal_feasible_grid_rows": feasible,
        "missing_energy_balance_grid_rows": 45,
        "comparison_cases": 5,
        "validation_metrics_recalculated": computed,
        "knee_hydraulic_power_reduction_percent": saving,
        "knee_temperature_penalty_C": penalty,
        "scope": "Evidence/data checks only; no new CFD, training, optimization, or hardware test.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, help="Optional checked summary output path.")
    args = parser.parse_args()
    report = review_project()
    print(f"PASS: {report['checks_passed']} Project 1 evidence/data checks")
    print("Grid: 45 cases; 36 train_cv / 9 labeled holdout; 19 satisfy Tmax <= 85 C.")
    for target, values in report["validation_metrics_recalculated"].items():
        print(f"{target}: MAE={values['MAE']:.8g}; max abs={values['Max_absolute_error']:.8g}; MAPE={values['MAPE_percent']:.6f}%")
    print(f"Balanced vs minimum-temperature candidate: {report['knee_hydraulic_power_reduction_percent']:.3f}% less hydraulic power; +{report['knee_temperature_penalty_C']:.3f} C.")
    print("LIMITATION: complete energy-balance fields absent from the 45-case/final confirmation evidence.")
    print(report["scope"])
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        print(f"Saved checked summary: {args.json_out.resolve()}")


if __name__ == "__main__":
    main()
