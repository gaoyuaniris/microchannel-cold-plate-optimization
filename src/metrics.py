"""Derived thermal-hydraulic metrics."""


def thermal_resistance(
    max_temperature_c: float,
    inlet_temperature_c: float,
    heat_load_w: float,
) -> float:
    if heat_load_w <= 0:
        raise ValueError("heat_load_w must be positive.")
    return (max_temperature_c - inlet_temperature_c) / heat_load_w


def pumping_power(pressure_drop_pa: float, flow_rate_l_min: float) -> float:
    if pressure_drop_pa < 0 or flow_rate_l_min < 0:
        raise ValueError("Pressure drop and flow rate cannot be negative.")
    return pressure_drop_pa * (flow_rate_l_min / 1000 / 60)


def chip_temperature_nonuniformity(
    max_temperature_c: float,
    min_temperature_c: float,
) -> float:
    if max_temperature_c < min_temperature_c:
        raise ValueError("Maximum temperature must be >= minimum temperature.")
    return max_temperature_c - min_temperature_c
