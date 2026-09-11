> **Historical Day 2 model-development notes.** These notes document the earlier 0.50 × 0.50 mm square-channel baseline, including its development-stage dimensions and future plans. They do not specify the final 0.30 × 0.70 mm geometry. Any differences between early notes are preserved rather than silently reconciled.
>
> [Current study](../README.md) · [History and provenance](../docs/history/README.md)

# Day 2 — Conjugate Heat Transfer Model Development

## Project Title

**Physics-Based and Machine-Learning-Assisted Optimization of a Microchannel Cold Plate for High-Heat-Flux Electronics**

## Day 2 Objective

The objective of Day 2 was to build the baseline three-dimensional conjugate heat transfer model for a liquid-cooled microchannel cold plate.

The model combines:

- heat generation in a silicon chip;
- conduction through a thermal interface material;
- heat spreading through copper;
- heat conduction through the cold plate;
- laminar water flow through ten parallel microchannels;
- convective heat transport in the coolant;
- pressure-drop prediction.

The baseline model will later be used for parametric optimization and machine-learning-assisted design.

---

## 1. Baseline Geometry

The model contains five main regions:

1. Silicon chip
2. Thermal interface material
3. Copper heat spreader
4. Copper cold plate
5. Ten rectangular water channels

### Geometry dimensions

| Component | Length | Width | Height or Thickness |
|---|---:|---:|---:|
| Silicon chip | 10 mm | 10 mm | 0.5 mm |
| TIM | 10 mm | 10 mm | 0.1 mm |
| Copper spreader | 12 mm | 12 mm | 1.0 mm |
| Cold plate | 30 mm | 30 mm | 3.0 mm |
| Each channel | 30 mm | 0.5 mm | 0.5 mm |

### Channel configuration

| Parameter | Value |
|---|---:|
| Number of channels | 10 |
| Channel width | 0.5 mm |
| Channel height | 0.5 mm |
| Channel pitch | 1.0 mm |
| Channel length | 30 mm |
| Bottom-wall thickness | 1.25 mm |

The channel length was set equal to the cold-plate length for the simplified baseline model.

This allows each channel to connect directly from the inlet face to the outlet face without adding inlet and outlet manifolds.

A later model version will add manifolds and may return to a shorter active channel length.

---

## 2. Vertical Layer Arrangement

The model uses the following vertical coordinates:

| Region | z-coordinate range |
|---|---:|
| Cold plate | 0 to 3.0 mm |
| Water channels | 1.25 to 1.75 mm |
| Copper spreader | 3.0 to 4.0 mm |
| TIM | 4.0 to 4.1 mm |
| Silicon chip | 4.1 to 4.6 mm |

The chip, TIM, spreader, and cold plate are centered with respect to the x- and y-directions.

---

## 3. Geometry Construction Method

The geometry was created using parameterized COMSOL blocks and Boolean operations.

### Geometry sequence

1. Create the copper cold-plate block.
2. Create one rectangular channel.
3. Generate a ten-channel linear array.
4. Subtract the channel array from the cold plate.
5. Keep the subtracted channel objects so they remain as fluid domains.
6. Add the copper spreader.
7. Add the TIM layer.
8. Add the silicon chip.
9. Finalize the geometry using Form Union.
10. Keep interior boundaries.

### Important Difference setting

For the Boolean Difference operation:

- Objects to add: cold plate
- Objects to subtract: channel array
- Keep objects to subtract: enabled
- Keep interior boundaries: enabled

Keeping the channel objects is necessary because the channels must exist as three-dimensional water domains.

---

## 4. Global Parameters

The main model parameters are:

| Parameter | Expression | Description |
|---|---|---|
| `Q_chip` | `100[W]` | Total chip heat generation |
| `T_in` | `25[degC]` | Coolant inlet temperature |
| `Vdot_total` | `0.2[l/min]` | Total coolant volumetric flow rate |
| `p_out` | `0[Pa]` | Outlet gauge pressure |
| `N_ch` | `10` | Number of channels |
| `w_ch` | `0.5[mm]` | Channel width |
| `h_ch` | `0.5[mm]` | Channel height |
| `L_ch` | `L_plate` | Channel length |
| `k_TIM` | `3[W/(m*K)]` | TIM thermal conductivity |
| `rho_TIM` | `2500[kg/m^3]` | TIM density |
| `Cp_TIM` | `1000[J/(kg*K)]` | TIM heat capacity |
| `T_limit` | `85[degC]` | Maximum desired chip temperature |

---

## 5. Material Assignment

The model uses four materials.

### Copper

Assigned to:

- cold plate;
- heat spreader.

Important properties include:

- thermal conductivity;
- density;
- heat capacity.

### Silicon

Assigned to:

- silicon chip only.

### Water, Liquid

Assigned to:

- ten channel domains only.

The built-in COMSOL liquid-water material supplies:

- density;
- dynamic viscosity;
- thermal conductivity;
- heat capacity.

### Effective TIM

Assigned to:

- thin layer between the silicon chip and copper spreader.

The custom TIM material uses:

| Property | Value |
|---|---:|
| Thermal conductivity | 3 W/(m·K) |
| Density | 2500 kg/m³ |
| Heat capacity | 1000 J/(kg·K) |

Dynamic viscosity is not required for the TIM because it is modeled as a stationary solid.

---

## 6. Physics Interfaces

The model uses:

1. Laminar Flow
2. Heat Transfer in Solids and Fluids
3. Nonisothermal Flow multiphysics coupling

---

## 7. Laminar Flow Setup

The Laminar Flow interface is restricted to the ten water-channel domains.

The parent physics selection was changed from:

`All domains`

to:

`Manual selection`

Only the ten fluid domains were selected.

The default Fluid Properties node continues to display:

`All domains`

This means all domains contained in the parent Laminar Flow selection, not all domains in the complete model.

### Fluid properties

The water properties are obtained from the assigned material:

- Density: From material
- Dynamic viscosity: From material

### Expected boundary conditions

The flow model will use:

- inlet condition on ten channel inlet faces;
- outlet pressure on ten channel outlet faces;
- no-slip condition on channel walls.

---

## 8. Heat Transfer Setup

The Heat Transfer in Solids and Fluids interface contains:

- Solid 1
- Fluid 1
- Thermal Insulation 1
- Initial Values 1

### Solid domains

The solid formulation applies to:

- silicon chip;
- TIM;
- copper spreader;
- copper cold plate.

### Fluid domains

The Fluid 1 feature applies to:

- ten water-channel domains.

The default Solid 1 feature may initially show all domains.

The Fluid 1 feature overrides the solid heat-transfer formulation in the selected channel domains.

---

## 9. Nonisothermal Flow Coupling

The Nonisothermal Flow feature couples:

- Laminar Flow;
- Heat Transfer in Solids and Fluids.

The coupling applies to the ten water-channel domains.

This allows the model to account for:

- heat convection by the coolant velocity;
- temperature-dependent water properties;
- coupled pressure, velocity, and temperature fields.

---

## 10. Meaning of Conjugate Heat Transfer

The model solves heat conduction in the solid domains and heat conduction plus convection in the fluid domains.

In the solids, the stationary heat equation is approximately:

\[
\nabla \cdot (k \nabla T) + Q = 0
\]

In the fluid, the energy equation is approximately:

\[
\rho C_p(\mathbf{u}\cdot\nabla T)
=
\nabla\cdot(k\nabla T)
\]

At the solid-fluid interface, COMSOL enforces continuity of temperature and heat flux.

This method avoids prescribing an empirical convection coefficient.

Instead, the local heat transfer is calculated from the solved velocity and temperature fields.

---

## 11. Heat Source

The baseline chip dissipates:

\[
Q_{\text{chip}} = 100\text{ W}
\]

The chip area is:

\[
A_{\text{chip}}
=
10\text{ mm}\times10\text{ mm}
=
100\text{ mm}^2
=
1.0\times10^{-4}\text{ m}^2
\]

The corresponding heat flux is:

\[
q''
=
\frac{Q_{\text{chip}}}{A_{\text{chip}}}
=
1.0\times10^6\text{ W/m}^2
\]

Therefore, the baseline chip heat flux is:

\[
\boxed{1.0\text{ MW/m}^2}
\]

The heat source may be implemented as either:

- a total volumetric heat source in the silicon chip; or
- a boundary heat source applied to the chip surface.

For the baseline model, a volumetric heat source is preferred because it represents internal heat generation within the chip domain.

The chip volume is:

\[
V_{\text{chip}}
=
10\text{ mm}
\times
10\text{ mm}
\times
0.5\text{ mm}
=
5.0\times10^{-8}\text{ m}^3
\]

The corresponding volumetric heat source is:

\[
Q_v
=
\frac{100}
{5.0\times10^{-8}}
=
2.0\times10^9\text{ W/m}^3
\]

---

## 12. Baseline Analytical Calculations

### Total channel flow area

The area of one channel is:

\[
A_{\text{ch}}
=
w_{\text{ch}}h_{\text{ch}}
=
0.5\text{ mm}\times0.5\text{ mm}
=
0.25\text{ mm}^2
\]

For ten channels:

\[
A_{\text{flow,total}}
=
10(0.25)
=
2.5\text{ mm}^2
=
2.5\times10^{-6}\text{ m}^2
\]

### Average channel velocity

The total volumetric flow rate is:

\[
\dot V
=
0.2\text{ L/min}
=
3.333\times10^{-6}\text{ m}^3/\text{s}
\]

Therefore:

\[
u_{\text{avg}}
=
\frac{\dot V}{A_{\text{flow,total}}}
\approx
1.33\text{ m/s}
\]

### Hydraulic diameter

For a rectangular channel:

\[
D_h
=
\frac{2wh}{w+h}
\]

For the square channel:

\[
D_h
=
0.5\text{ mm}
\]

### Reynolds number

Using water properties near 25°C:

\[
Re
=
\frac{\rho uD_h}{\mu}
\approx
750
\]

The expected flow regime is laminar.

### Coolant temperature rise

The coolant temperature increase can be estimated from:

\[
Q
=
\dot m C_p \Delta T
\]

Using the total flow rate and water properties:

\[
\Delta T_{\text{water}}
\approx
7.2^\circ\text{C}
\]

Therefore, the expected outlet bulk temperature is:

\[
T_{\text{out}}
\approx
25+7.2
=
32.2^\circ\text{C}
\]

### Pressure drop

The expected straight-channel pressure drop is approximately:

\[
\Delta p
\approx
4.0\text{ kPa}
\]

This estimate was adjusted from the earlier 25 mm channel design to the current 30 mm channel length.

### Hydraulic pumping power

\[
P_{\text{hydraulic}}
=
\Delta p\dot V
\]

\[
P_{\text{hydraulic}}
\approx
0.0135\text{ W}
\]

This represents ideal hydraulic power and does not include real pump inefficiency.

---

## 13. TIM Thermal Resistance Estimate

The approximate one-dimensional TIM resistance is:

\[
R_{\text{TIM}}
=
\frac{t_{\text{TIM}}}
{k_{\text{TIM}}A_{\text{TIM}}}
\]

Using:

- thickness = 0.1 mm;
- conductivity = 3 W/(m·K);
- area = 10 mm × 10 mm;

the result is:

\[
R_{\text{TIM}}
\approx
0.333\text{ K/W}
\]

At 100 W, the approximate TIM temperature drop is:

\[
\Delta T_{\text{TIM}}
=
Q R_{\text{TIM}}
\approx
33.3^\circ\text{C}
\]

This indicates that the TIM may contribute a large fraction of the total system thermal resistance.

A future study should evaluate TIM thickness and conductivity.

---

## 14. Expected Baseline Results

Before accepting the COMSOL solution, the following approximate values will be checked:

| Quantity | Expected value |
|---|---:|
| Chip heat flux | 1.0 MW/m² |
| Channel-average velocity | 1.33 m/s |
| Hydraulic diameter | 0.5 mm |
| Reynolds number | Approximately 750 |
| Coolant temperature rise | Approximately 7.2°C |
| Bulk outlet temperature | Approximately 32.2°C |
| Pressure drop | Approximately 4.0 kPa |
| Hydraulic pumping power | Approximately 0.0135 W |
| TIM thermal resistance | Approximately 0.333 K/W |

---

## 15. Performance Metrics

### Maximum chip temperature

The first thermal performance metric is:

\[
T_{\max,\text{chip}}
\]

The design goal is:

\[
T_{\max,\text{chip}}
\leq
85^\circ\text{C}
\]

### System thermal resistance

The system thermal resistance is defined as:

\[
R_{\text{th,system}}
=
\frac{T_{\max,\text{chip}}-T_{\text{inlet}}}
{Q_{\text{chip}}}
\]

For the target temperature:

\[
R_{\text{th,target}}
=
\frac{85-25}{100}
=
0.60\text{ K/W}
\]

Therefore, the design objective is:

\[
R_{\text{th,system}}
\leq
0.60\text{ K/W}
\]

### Pressure drop

The flow penalty will be evaluated using:

\[
\Delta p
=
p_{\text{inlet}}-p_{\text{outlet}}
\]

### Pumping power

\[
P_{\text{pump}}
=
\Delta p\dot V
\]

The final optimization will seek low chip temperature and low pumping power.

---

## 16. Modeling Assumptions

The baseline model assumes:

1. Steady-state operation.
2. Single-phase liquid water.
3. Laminar incompressible flow.
4. No phase change or boiling.
5. Perfect thermal contact between the solid layers.
6. Isotropic material properties.
7. Uniform chip heat generation.
8. Equal channel dimensions.
9. Direct channel inlet and outlet without manifolds.
10. No coolant leakage.
11. No radiation heat transfer.
12. External surfaces are thermally insulated unless otherwise specified.
13. Water properties may vary with temperature through the built-in material model.
14. Surface roughness is neglected.
15. Gravitational and buoyancy effects are neglected.

---

## 17. Current Simulation Status

The baseline model currently includes:

- completed parameterized geometry;
- retained water-channel domains;
- assigned copper, silicon, water, and TIM materials;
- Laminar Flow restricted to channel domains;
- Heat Transfer in Solids and Fluids;
- Nonisothermal Flow coupling.

Current computation status:

`Simulation running / results pending`

This section will be updated after convergence.

---

## 18. Results to Record

After the simulation finishes, record:

| Metric | COMSOL result | Analytical estimate | Difference |
|---|---:|---:|---:|
| Maximum chip temperature | TBD | N/A | N/A |
| Average outlet temperature | TBD | 32.2°C | TBD |
| Pressure drop | TBD | 4.0 kPa | TBD |
| Average channel velocity | TBD | 1.33 m/s | TBD |
| Reynolds number | TBD | 750 | TBD |
| System thermal resistance | TBD | Target ≤ 0.60 K/W | TBD |
| Hydraulic pumping power | TBD | 0.0135 W | TBD |

---

## 19. Result Validation Checklist

The solution will not be accepted based only on numerical convergence.

The following checks will be completed:

- [ ] Maximum chip temperature is physically reasonable.
- [ ] Average channel velocity is close to 1.33 m/s.
- [ ] Bulk coolant outlet temperature is close to 32.2°C.
- [ ] Pressure drop is close to the analytical estimate.
- [ ] The velocity is zero at no-slip walls.
- [ ] The temperature increases from inlet to outlet.
- [ ] Heat flows from the chip toward the coolant.
- [ ] No unexpected thermal discontinuity appears between bonded solids.
- [ ] All ten channels carry flow.
- [ ] No channel shows reverse flow.
- [ ] Energy leaving through the coolant is close to 100 W.
- [ ] Mesh refinement produces stable temperature and pressure-drop results.

---

## 20. Initial Mesh-Independence Plan

At least three mesh levels will be tested:

| Mesh level | Maximum chip temperature | Pressure drop | Element count |
|---|---:|---:|---:|
| Coarse | TBD | TBD | TBD |
| Normal | TBD | TBD | TBD |
| Fine | TBD | TBD | TBD |

The preliminary convergence target is:

- less than 2% change in maximum chip temperature;
- less than 5% change in pressure drop.

Pressure drop is expected to be more mesh-sensitive than the maximum solid temperature.

---

## 21. Planned Parametric Studies

The following parameters will be varied in later stages:

### Channel geometry

- channel width;
- channel height;
- number of channels;
- channel pitch;
- bottom-wall thickness;
- channel length.

### Operating conditions

- chip power;
- coolant flow rate;
- inlet temperature.

### TIM design

- TIM thermal conductivity;
- TIM thickness.

### Candidate outputs

- maximum chip temperature;
- average chip temperature;
- temperature uniformity;
- coolant outlet temperature;
- pressure drop;
- pumping power;
- system thermal resistance.

---

## 22. Relevance to Thermal Engineering Jobs

This project demonstrates experience in:

- electronics cooling;
- liquid-cooled cold-plate design;
- conjugate heat transfer;
- computational fluid dynamics;
- pressure-drop analysis;
- thermal resistance modeling;
- material-property assignment;
- thermal interface analysis;
- simulation verification;
- mesh-independence studies;
- parametric optimization;
- design tradeoff analysis;
- preparation for surrogate and machine-learning modeling.

The project is intended to support applications for roles such as:

- Thermal Engineer
- Electronics Cooling Engineer
- Thermal Mechanical Engineer
- Data Center Cooling Engineer
- Server Thermal Engineer
- Cold Plate Design Engineer
- Thermal Simulation Engineer
- Hardware Validation Engineer

---

## 23. Key Day 2 Learning Outcomes

The main lessons from Day 2 were:

1. A fluid volume must remain in the geometry for CFD analysis.
2. Boolean subtraction alone can remove the channel object unless it is retained.
3. Material assignment is performed at the domain level.
4. Dynamic viscosity is required for water but not for a solid TIM.
5. The Laminar Flow parent selection controls where velocity and pressure are solved.
6. Default child nodes may display all domains but inherit the parent physics selection.
7. Fluid heat transfer overrides the default solid formulation in selected water domains.
8. Conjugate heat transfer directly solves solid conduction and fluid convection.
9. Analytical calculations are required to validate the numerical model.
10. TIM resistance can be a major contributor to chip temperature.

---

## 24. Next Steps

The next steps are:

1. Complete the baseline simulation.
2. Check convergence messages.
3. Calculate maximum chip temperature.
4. Calculate bulk outlet temperature.
5. Calculate pressure drop.
6. Calculate system thermal resistance.
7. Check the energy balance.
8. Create temperature, velocity, pressure, and streamline plots.
9. Perform mesh-independence testing.
10. Begin the first flow-rate parametric sweep.