from src.validation import validate_record


def test_valid_record():
    row = {
        "case_id": "baseline",
        "heat_load_W": 100,
        "flow_rate_L_min": 0.2,
        "inlet_temperature_C": 25,
        "max_chip_temperature_C": 65,
        "pressure_drop_Pa": 3500,
        "energy_balance_error_percent": 1.0,
        "solver_converged": True,
    }
    assert validate_record(row) == []
