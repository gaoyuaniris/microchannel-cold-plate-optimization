# Design Specification

## Problem

A compact 10 mm × 10 mm heat source produces up to 200 W. A water-cooled microchannel cold plate should maintain the chip below a selected temperature limit while minimizing pressure drop and pumping power.

## Baseline

- Silicon chip: 10 × 10 × 0.5 mm
- TIM: 10 × 10 × 0.10 mm, 3 W/(m·K)
- Copper spreader: 12 × 12 × 1 mm
- Copper cold plate: 30 × 30 × 3 mm
- Channels: 10
- Channel size: 0.50 × 0.50 × 25 mm
- Inlet temperature: 25 °C
- Heat load: 100 W
- Total flow: 0.20 L/min

## Project targets

- Maximum chip temperature ≤ 85 °C
- Thermal resistance ≤ 0.60 K/W
- Preferred optimized temperature: 75–80 °C or lower
- Preferred pressure drop ≤ 20 kPa
- Initial design-space flow ≤ 0.40 L/min

These are portfolio-project targets, not universal product requirements.

## Required outputs

- Maximum, average, and minimum chip temperature
- Coolant outlet temperature
- Pressure drop
- Thermal resistance
- Pumping power
- Reynolds number
- Energy-balance error
- Solver convergence status

## Acceptance criteria

- Solver converges
- Energy-balance error < 2% for production cases
- Medium-to-fine mesh change < 2% for maximum temperature
- Medium-to-fine mesh change < 3% for pressure drop
