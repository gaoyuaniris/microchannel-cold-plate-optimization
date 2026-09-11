> **Historical learning notes.** This learning material contains early estimates and planned questions for the 0.50 × 0.50 mm square-channel baseline. Expected values are not final simulation results. The final study uses 0.30 × 0.70 mm channels.
>
> [Current study](../README.md) · [History and provenance](../docs/history/README.md)

# Day 1 Learning Notes

## 1. Electronic Package Thermal Path

The simplified heat-transfer path is:

Chip → TIM → Heat Spreader → Cold Plate → Coolant

The chip generates heat. The TIM reduces interface resistance, the heat
spreader distributes heat over a larger area, and the cold plate transfers
heat into the flowing coolant.

## 2. Role of Each Component

### Chip

- Generates heat
- May contain localized hotspots
- Maximum junction temperature is an important design metric

### Thermal Interface Material

- Fills microscopic air gaps between surfaces
- Reduces thermal contact resistance
- Performance depends on conductivity and thickness

### Heat Spreader

- Distributes heat over a larger area
- Usually uses a high-conductivity material such as copper

### Cold Plate

- Conducts heat into the coolant
- Contains microchannels for liquid flow
- Geometry affects temperature and pressure drop

### Coolant

- Carries heat out of the system
- Water is used in the baseline model

## 3. Thermal Resistance Network

The simplified total thermal resistance is:

R_total = R_chip + R_TIM + R_spreader + R_plate + R_convection

For conduction through a flat layer:

R_cond = L / (kA)

For convection:

R_conv = 1 / (hA)

The chip temperature rise can be estimated using:

Delta_T = Q × R_total

## 4. TIM Resistance Calculation

Baseline TIM properties:

- Thickness = 100 micrometers
- Thermal conductivity = 3 W/(m·K)
- Area = 10 mm × 10 mm

Calculated TIM resistance:

R_TIM = 0.333 K/W

At 100 W:

Delta_T_TIM = 33.3 °C

This shows that TIM thickness and conductivity can strongly influence the
chip temperature.

## 5. Semiconductor Package Thermal Metrics

Important metrics include:

- R_theta_JA: junction-to-ambient thermal resistance
- R_theta_JC: junction-to-case thermal resistance
- R_theta_JB: junction-to-board thermal resistance
- Psi_JT: junction-to-top characterization parameter
- Psi_JB: junction-to-board characterization parameter

These values depend on the measurement and test conditions.

## 6. Thermal Contact Resistance

Real surfaces touch only at microscopic asperities. Air gaps between rough
surfaces increase thermal resistance.

TIM helps by filling these gaps and providing a more continuous heat-transfer
path.

## 7. Expected COMSOL Physics

The COMSOL model will use:

- Laminar Flow
- Heat Transfer in Solids and Fluids
- Nonisothermal Flow coupling

The model will calculate:

- Temperature distribution
- Coolant velocity
- Pressure drop
- Maximum chip temperature
- Coolant outlet temperature

## 8. Expected Baseline Results

- Heat flux: approximately 1 MW/m²
- Average channel velocity: approximately 1.33 m/s
- Reynolds number: approximately 750
- Outlet coolant temperature: approximately 32.2 °C
- Pressure drop: on the order of several kPa

## 9. Questions I Still Need to Answer

- Which part of the thermal path dominates the total resistance?
- How much does TIM thickness affect chip temperature?
- How does channel width affect pressure drop?
- How should the manifold geometry be designed?
- How closely will COMSOL agree with the hand calculations?


## Semiconductor Package Thermal Metrics

Thermal metrics must be interpreted according to their test conditions and
dominant heat-flow paths.

- RθJA describes junction-to-ambient performance for a package, PCB, and
  environment under defined test conditions. It is not a package-only constant.
- RθJC describes the junction-to-case path when heat is intentionally forced
  through the specified case surface, such as with an effective cold plate.
- ΨJT is a characterization parameter used to estimate junction temperature
  from a measured package-top temperature. It is not a true thermal resistance.
- RθJB describes a controlled junction-to-board thermal path.
- ΨJB estimates junction temperature from a measured board temperature under
  application-like heat-flow partitioning.

For the current cold-plate project, the primary metric will be the system
chip-to-coolant-inlet thermal resistance:

R_th,system = (T_max,chip - T_inlet) / Q

This project-specific metric will always be reported together with heat load,
coolant flow rate, inlet temperature, geometry, and boundary conditions.