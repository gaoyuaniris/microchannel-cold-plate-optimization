"""Load COMSOL-exported CSV files and add derived metrics."""

from pathlib import Path
import pandas as pd
from src.metrics import pumping_power, thermal_resistance

RAW_DIR = Path("comsol/exported_results")
OUTPUT_PATH = Path("data/processed/master_cases.csv")


def load_exports(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    files = sorted(raw_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir}.")
    return pd.concat([pd.read_csv(file) for file in files], ignore_index=True)


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["thermal_resistance_K_W"] = result.apply(
        lambda row: thermal_resistance(
            row["max_chip_temperature_C"],
            row["inlet_temperature_C"],
            row["heat_load_W"],
        ),
        axis=1,
    )
    result["pumping_power_W"] = result.apply(
        lambda row: pumping_power(
            row["pressure_drop_Pa"],
            row["flow_rate_L_min"],
        ),
        axis=1,
    )
    return result


def main() -> None:
    processed = add_derived_metrics(load_exports())
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(processed)} cases to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
