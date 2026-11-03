---
name: genpark-personal-agent-cutaneous-capillary-refill-time-ppi-shock-skill
version: 1.0.0
description: Calculates Capillary Refill Time (CRT), Peripheral Perfusion Index (PPI), and Microvascular Shock Index (MSI).
license: Apache-2.0
compatibility:
  python: ">=3.9"
  openclaw: ">=1.0.0"
  mcp: ">=1.0.0"
---

# Cutaneous Capillary Refill Time (CRT) & Peripheral Perfusion Index (PPI) Skill

A zero-dependency personal agent skill for evaluating peripheral cutaneous microvascular perfusion, cyclical vasoconstriction, and circulatory shock kinetics (ANDROMEDA-SHOCK criteria).

## Features
- **Capillary Refill Time ($CRT$)**: Quantifies microvascular reperfusion kinetics following standardized pressure blanching ($\le 2.5\text{ s}$ normal).
- **Peripheral Perfusion Index ($PPI\%$)**: Computes ratio of pulsatile photoelectric amplitude to non-pulsatile baseline ($AC / DC \times 100\%$).
- **Microvascular Shock Index ($MSI$)**: Calculates $CRT / PPI$ to amplify detection of occult tissue hypoperfusion.
- **Thermal Distinction**: Compares local skin temperature against systemic circulatory vasoconstriction.

## MCP Server Integration
Exposes `evaluate_microvascular_perfusion` for autonomous shock triage, fluid resuscitation monitoring, and peripheral vascular health assessment.
