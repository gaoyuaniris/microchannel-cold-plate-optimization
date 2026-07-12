"""Validation rules for COMSOL result rows."""

REQUIRED_COLUMNS = {
    "case_id",
    "heat_load_W",
    "flow_rate_L_min",
    "inlet_temperature_C",
    "max_chip_temperature_C",
    "pressure_drop_Pa",
    "energy_balance_error_percent",
    "solver_converged",
}


def validate_record(record: dict) -> list[str]:
    problems = []
    missing = REQUIRED_COLUMNS.difference(record)
    if missing:
        return [f"Missing columns: {sorted(missing)}"]

    if not bool(record["solver_converged"]):
        problems.append("Solver did not converge.")
    if float(record["heat_load_W"]) <= 0:
        problems.append("Heat load must be positive.")
    if float(record["flow_rate_L_min"]) <= 0:
        problems.append("Flow rate must be positive.")
    if float(record["pressure_drop_Pa"]) < 0:
        problems.append("Pressure drop cannot be negative.")
    if float(record["max_chip_temperature_C"]) < float(record["inlet_temperature_C"]):
        problems.append("Maximum chip temperature is below inlet temperature.")
    if abs(float(record["energy_balance_error_percent"])) > 2:
        problems.append("Energy-balance error exceeds 2%.")
    return problems
