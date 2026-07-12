"""Train starter surrogate models for maximum chip temperature."""

from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

FEATURES = [
    "heat_load_W",
    "flow_rate_L_min",
    "channel_width_mm",
    "channel_height_mm",
    "channel_count",
    "tim_conductivity_W_mK",
    "tim_thickness_um",
]
TARGET = "max_chip_temperature_C"


def main() -> None:
    df = pd.read_csv("data/processed/master_cases.csv").dropna(
        subset=FEATURES + [TARGET]
    )
    if len(df) < 20:
        raise ValueError("At least 20 valid simulation cases are recommended.")

    x_train, x_test, y_train, y_test = train_test_split(
        df[FEATURES], df[TARGET], test_size=0.2, random_state=42
    )
    models = {
        "linear": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=300, random_state=42, n_jobs=-1
        ),
        "gradient_boosting": GradientBoostingRegressor(random_state=42),
    }
    Path("models").mkdir(exist_ok=True)

    for name, model in models.items():
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        rmse = mean_squared_error(y_test, pred) ** 0.5
        print(
            f"{name}: MAE={mean_absolute_error(y_test, pred):.3f}, "
            f"RMSE={rmse:.3f}, R2={r2_score(y_test, pred):.3f}"
        )
        joblib.dump(model, f"models/{name}_temperature.joblib")


if __name__ == "__main__":
    main()
