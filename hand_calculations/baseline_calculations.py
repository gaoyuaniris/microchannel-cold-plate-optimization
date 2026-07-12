"""Baseline engineering calculations for the microchannel cold-plate project."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Inputs:
    chip_power_w: float = 100.0
    chip_length_m: float = 0.010
    chip_width_m: float = 0.010
    total_flow_l_min: float = 0.20
    channel_count: int = 10
    channel_width_m: float = 0.0005
    channel_height_m: float = 0.0005
    channel_length_m: float = 0.025
    inlet_temperature_c: float = 25.0
    max_temperature_limit_c: float = 85.0
    water_density_kg_m3: float = 997.0
    water_viscosity_pa_s: float = 0.00089
    water_cp_j_kg_k: float = 4180.0


def calculate(i: Inputs) -> dict[str, float]:
    if i.channel_count <= 0 or i.total_flow_l_min <= 0:
        raise ValueError("Channel count and flow rate must be positive.")

    chip_area = i.chip_length_m * i.chip_width_m
    heat_flux = i.chip_power_w / chip_area
    total_flow = i.total_flow_l_min / 1000 / 60
    flow_per_channel = total_flow / i.channel_count
    mass_flow = i.water_density_kg_m3 * total_flow
    coolant_rise = i.chip_power_w / (mass_flow * i.water_cp_j_kg_k)

    total_flow_area = (
        i.channel_count * i.channel_width_m * i.channel_height_m
    )
    velocity = total_flow / total_flow_area
    hydraulic_diameter = (
        2 * i.channel_width_m * i.channel_height_m
        / (i.channel_width_m + i.channel_height_m)
    )
    reynolds = (
        i.water_density_kg_m3 * velocity * hydraulic_diameter
        / i.water_viscosity_pa_s
    )
    darcy_f = 56.91 / reynolds
    pressure_drop = (
        darcy_f
        * (i.channel_length_m / hydraulic_diameter)
        * (i.water_density_kg_m3 * velocity**2 / 2)
    )
    pumping_power = pressure_drop * total_flow
    target_rth = (
        i.max_temperature_limit_c - i.inlet_temperature_c
    ) / i.chip_power_w

    return {
        "chip_area_m2": chip_area,
        "heat_flux_w_m2": heat_flux,
        "total_flow_m3_s": total_flow,
        "flow_per_channel_m3_s": flow_per_channel,
        "coolant_temperature_rise_c": coolant_rise,
        "estimated_outlet_temperature_c": i.inlet_temperature_c + coolant_rise,
        "average_channel_velocity_m_s": velocity,
        "hydraulic_diameter_m": hydraulic_diameter,
        "reynolds_number": reynolds,
        "darcy_friction_factor": darcy_f,
        "straight_channel_pressure_drop_pa": pressure_drop,
        "hydraulic_pumping_power_w": pumping_power,
        "target_thermal_resistance_k_w": target_rth,
    }


def main() -> None:
    inputs = Inputs()
    results = calculate(inputs)
    for key, value in results.items():
        print(f"{key}: {value:.6g}")

    output = {"inputs": asdict(inputs), "results": results}
    path = Path(__file__).with_name("baseline_results.json")
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
