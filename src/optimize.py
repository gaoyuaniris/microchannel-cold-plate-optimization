"""Two-objective Pareto-front extraction."""

import pandas as pd


def pareto_front(
    df: pd.DataFrame,
    objective_x: str = "max_chip_temperature_C",
    objective_y: str = "pumping_power_W",
) -> pd.DataFrame:
    ordered = df.sort_values([objective_x, objective_y]).copy()
    best_y = float("inf")
    keep = []
    for index, row in ordered.iterrows():
        if float(row[objective_y]) < best_y:
            keep.append(index)
            best_y = float(row[objective_y])
    return ordered.loc[keep].reset_index(drop=True)
