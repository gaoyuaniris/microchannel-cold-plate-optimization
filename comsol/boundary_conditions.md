> **Early setup notes.** This is an initial boundary-condition checklist for the earlier 0.50 × 0.50 mm square-channel baseline, not a record of every final COMSOL setting. The final study uses 0.30 × 0.70 mm channels.
>
> [Current study](../README.md) · [History and provenance](../docs/history/README.md)

# Boundary Conditions

## Flow
- Inlet: specified total volumetric flow
- Outlet: zero gauge pressure
- Walls: no slip

## Thermal
- Chip: total power or volumetric heat source
- Coolant inlet: 25 °C
- Internal interfaces: thermal continuity
- External plate surfaces: adiabatic for baseline
- TIM: explicit solid layer

## Verification
- Mass conservation
- Energy balance
- Mesh independence
- Expected thermal and hydraulic trends
