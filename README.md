# Cutaneous Capillary Refill Time (CRT) & Peripheral Perfusion Index (PPI) Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](requirements.txt)
[![Status: Production-Ready](https://img.shields.io/badge/status-production--ready-success.svg)](https://github.com/alphaparkinc)

A zero-dependency, mathematically rigorous personal agent skill that computes cutaneous capillary refill time, pulse oximetry perfusion index, and microvascular shock indices to evaluate peripheral tissue perfusion.

## Architecture

```mermaid
flowchart TD
    A[Photometric Blanching / Infrared PPG Probe] --> B[Measure Capillary Refill Time CRT & AC/DC Ratio]
    B --> C[Compute Peripheral Perfusion Index PPI = AC/DC * 100]
    C --> D[Compute Microvascular Shock Index MSI = CRT / PPI]
    D --> E[Benchmark vs ANDROMEDA-SHOCK Resuscitation Criteria]
    E --> F[Circulatory Shock & Vasoconstriction Guidance]
```

## Quick Start

```python
from client import CapillaryRefillPerfusionClient

client = CapillaryRefillPerfusionClient()
result = client.evaluate_microvascular_perfusion(
    capillary_refill_time_seconds=1.7,
    pulsatile_ac_signal=22.0,
    baseline_dc_signal=1000.0
)
print("CRT (s):", result["microvascular_metrics"]["capillary_refill_time_crt_seconds"])
print("PPI (%):", result["microvascular_metrics"]["peripheral_perfusion_index_ppi_pct"])
print("Status:", result["perfusion_assessment"]["perfusion_state"])
```

## License
Apache-2.0
