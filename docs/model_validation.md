# Model Validation

## 1. Validation Objective

The microchannel cold-plate model was validated before beginning the geometry optimization and machine-learning stages.

The validation focused on:

1. Coolant-flow consistency
2. Mass conservation
3. Heat-source verification
4. Heat and total-energy conservation
5. Mesh independence
6. Computationally efficient mesh selection

The primary validation operating condition was:

| Parameter | Value |
|---|---:|
| Total coolant flow rate | 0.25 L/min |
| Coolant inlet temperature | 25°C |
| Chip heat load | 100 W |
| Number of microchannels | 10 |
| Channel cross section | 0.5 mm × 0.5 mm |
| Total channel flow area | 2.50 × 10⁻⁶ m² |

---

## 2. Coolant-Flow Boundary Verification

### Initial setup

The original inlet condition used a prescribed velocity:

$$
u_{\mathrm{in}}
=
\frac{\dot V_{\mathrm{total}}}
{A_{\mathrm{flow,total}}}
$$

Although the inlet and outlet flow rates were equal, the calculated flow was approximately 87.5% of the intended value.

This showed that the model conserved mass, but the velocity boundary condition did not impose the desired total integrated flow accurately for this configuration.

### Corrected setup

The inlet was changed to:

```text
Laminar Flow
→ Inlet
→ Fully Developed Flow
→ Flow Rate
```

Because the model contains ten disconnected channel inlets, the flow assigned to each channel was:

$$
\dot V_{\mathrm{channel}}
=
\frac{\dot V_{\mathrm{total}}}{N_{\mathrm{ch}}}
$$

The option to apply the condition separately to each disconnected inlet was enabled.

The outlet remained a pressure boundary:

```text
Outlet pressure = 0 Pa
```

### Flow validation results

The inlet and outlet integration selections both included all ten channel faces:

$$
A_{\mathrm{in}}
\approx
A_{\mathrm{out}}
\approx
2.50\times10^{-6}\ \mathrm{m^2}
$$

After correcting the inlet condition:

$$
\dot V_{\mathrm{in}}
\approx
\dot V_{\mathrm{out}}
\approx
\dot V_{\mathrm{total}}
$$

Therefore, the final model satisfies volumetric-flow conservation and delivers the requested coolant flow rate.

---

## 3. Chip Heat-Source Verification

The chip heat load was applied as a volumetric heat source:

$$
Q'''_{\mathrm{chip}}
=
\frac{Q_{\mathrm{chip}}}{V_{\mathrm{chip}}}
$$

The total heat source was independently checked by integrating the volumetric source over the chip domain:

$$
\int_{V_{\mathrm{chip}}}Q'''_{\mathrm{chip}}\,dV
\approx
100\ \mathrm{W}
$$

At the 0.25 L/min validation condition, COMSOL reported:

| Quantity | Result |
|---|---:|
| Integrated chip heat source | 99.992 W |
| Intended chip heat load | 100 W |

The relative difference was approximately 0.008%, confirming that the chip-domain selection, chip volume, and volumetric heat-source definition were correct.

---

## 4. Heat and Energy Balance

COMSOL's native heat- and total-energy-balance variables were evaluated for the stationary conjugate heat-transfer solution.

At 0.25 L/min:

| Quantity | Result |
|---|---:|
| Total heat source | 99.992 W |
| Heat-balance residual | −0.07107 W |
| Total-energy-balance residual | −0.07310 W |
| Relative heat-balance error | 0.0711% |
| Relative energy-balance error | 0.0731% |

The errors were calculated as:

$$
\epsilon_{\mathrm{heat}}
=
\frac{|\mathrm{Heat\ Balance}|}
{\mathrm{Total\ Heat\ Source}}
\times100\%
$$

$$
\epsilon_{\mathrm{energy}}
=
\frac{|\mathrm{Energy\ Balance}|}
{\mathrm{Total\ Heat\ Source}}
\times100\%
$$

Across the complete flow-rate sweep, the heat- and energy-balance residuals remained below approximately 0.14 W, corresponding to errors below approximately 0.14%.

These results confirm that:

- the 100 W chip heat source is correctly applied;
- the stationary solver is well converged;
- the external thermal-insulation condition does not introduce a significant energy loss;
- the conjugate heat-transfer model conserves heat and total energy.

A preliminary calculation using

$$
\dot Q
=
\dot m C_p
\left(T_{\mathrm{out}}-T_{\mathrm{in}}\right)
$$

underestimated the heat removal because it represented a simplified sensible-energy calculation. COMSOL's native energy balance was therefore used as the primary conservation check.

---

## 5. Preliminary Automatic-Mesh Study

An initial mesh study was performed using COMSOL's physics-controlled automatic mesh presets:

```text
Coarse
Normal
Finer
Extremely Fine
```

The total element count increased as expected, and the following quantities were stable:

- average chip temperature;
- coolant outlet temperature;
- pressure drop;
- pumping power;
- inlet and outlet flow rates;
- heat and total-energy balance.

However, the pointwise maximum chip temperature varied nonmonotonically between the automatic mesh levels.

The average chip temperature remained nearly unchanged, indicating that the overall temperature field was converged. The remaining variation was localized to the maximum-temperature region near the chip–TIM thermal stack.

This indicated local hotspot sensitivity rather than a global physics or conservation problem.

---

## 6. Local Thermal-Stack Mesh Refinement

The mesh was changed to a user-controlled sequence while retaining the automatically generated fluid-domain sizing, channel-wall refinement, and boundary-layer controls.

Additional local size controls were applied to:

- the chip domain;
- the thermal interface material;
- the copper spreader;
- the chip–TIM and TIM–spreader regions.

The TIM mesh was specifically refined because it is only 0.1 mm thick and directly controls heat conduction from the chip to the cold plate.

The final strategy used:

```text
Global background mesh: Normal
Local refinement: chip–TIM–spreader region
Existing fluid and boundary-layer controls: retained
```

This approach provided higher resolution near the thermal hotspot without unnecessarily refining the entire cold plate.

---

## 7. Final Mesh-Independence Results

After adding the local thermal-stack refinement, the maximum chip temperatures were:

| Mesh level | Maximum chip temperature | Thermal resistance |
|---|---:|---:|
| Coarse | 87.653°C | 0.62653 K/W |
| Normal | 87.704°C | 0.62704 K/W |
| Fine | 87.614°C | 0.62614 K/W |

Thermal resistance was calculated as:

$$
R_{\mathrm{th}}
=
\frac{T_{\max}-T_{\mathrm{in}}}
{Q_{\mathrm{chip}}}
$$

### Maximum-temperature convergence

The total maximum-temperature spread was:

$$
87.704-87.614
=
0.090^\circ\mathrm{C}
$$

The normal-to-fine difference was:

$$
|87.704-87.614|
=
0.090^\circ\mathrm{C}
$$

or approximately:

$$
0.103\%
$$

### Thermal-resistance convergence

The normal-to-fine thermal-resistance difference was approximately:

$$
0.14\%
$$

Both values were well below the selected acceptance limits:

| Validation metric | Acceptance criterion | Result |
|---|---:|---:|
| Maximum-temperature difference | < 0.5°C | 0.090°C |
| Maximum-temperature relative difference | < 1% | 0.103% |
| Thermal-resistance difference | < 1% | 0.14% |
| Heat-balance error | < 1% | approximately 0.07% |
| Energy-balance error | < 1% | approximately 0.07% |

The small nonmonotonic variation between the final mesh levels is negligible because all three predictions are within 0.1°C.

---

## 8. Selected Production Mesh

The normal global mesh with local chip–TIM–spreader refinement was selected for subsequent studies.

This mesh was selected because it:

- produced practically the same maximum temperature as the fine mesh;
- satisfied the thermal mesh-independence criteria;
- maintained excellent mass and energy conservation;
- required less computational effort than the fine mesh;
- provided targeted resolution in the region controlling the thermal hotspot.

The fine locally refined mesh was retained as the verification reference.

The selected mesh will remain fixed during subsequent geometry design-of-experiments simulations and machine-learning dataset generation. This prevents changes in mesh resolution from introducing artificial variation into the simulation outputs.

---

## 9. Design Implication

The validated maximum chip temperature at 0.25 L/min is approximately:

$$
T_{\max}
\approx
87.7^\circ\mathrm{C}
$$

This exceeds the design requirement:

$$
T_{\max}
\leq
85^\circ\mathrm{C}
$$

Therefore, the earlier conclusion that 0.25 L/min was acceptable was influenced by insufficient local thermal-stack resolution.

The coolant flow-rate sweep must be regenerated using the selected validated mesh. The minimum acceptable flow rate may shift to 0.30 L/min or higher.

---

## 10. Final Validation Conclusion

The microchannel cold-plate model was verified using flow-rate checks, mass conservation, integrated heat-source evaluation, native COMSOL heat and energy balances, and a targeted mesh-independence study.

The final model demonstrated:

- correct prescribed coolant flow;
- agreement between inlet and outlet flow rates;
- an applied chip heat load of approximately 100 W;
- heat- and energy-balance errors below approximately 0.14%;
- maximum-temperature variation below 0.1°C after local refinement;
- thermal-resistance variation below 0.2% between the normal and fine locally refined meshes.

The normal mesh with targeted chip–TIM–spreader refinement was therefore selected as the validated production mesh for the remaining optimization and machine-learning stages.
