> **Early modeling assumptions.** This initial checklist accompanies the earlier 0.50 × 0.50 mm square-channel baseline. It is retained as development context, not a complete verified specification of the final 0.30 × 0.70 mm study.
>
> [Current study](../README.md) · [History and provenance](../docs/history/README.md)

# Modeling Assumptions

## Flow
- Single-phase incompressible water
- Laminar flow
- No slip at walls
- Specified total inlet flow
- Zero-gauge-pressure outlet
- Gravity, boiling, and cavitation neglected

## Thermal
- Temperature-dependent water properties when available
- Isotropic solids
- Uniform chip heat generation
- Explicit TIM layer
- Radiation neglected
- External cold-plate surfaces adiabatic in the baseline
- Stationary primary study

## Geometry
- Identical straight parallel channels
- Simplified manifolds
- No roughness, leakage, or deformation

## Numerical
- Stationary solver first
- Refine mesh in channels and thin layers
- Exclude failed or nonphysical cases from ML training
