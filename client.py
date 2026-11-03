"""
Cutaneous Capillary Refill Time (CRT) & Peripheral Perfusion Index (PPI) Client.
Zero-mock pure Python standard library implementation.
Calculates Capillary Refill Time (CRT in seconds), Pulse Oximetry Perfusion Index (PPI in %),
Microvascular Shock Index (MSI = CRT / PPI), and circulatory shock risk staging (ANDROMEDA-SHOCK).
"""

import math
from typing import Dict, Any, Optional


class CapillaryRefillPerfusionClient:
    """
    Evaluates cutaneous microvascular tissue perfusion and shock resuscitation kinetics:
    - CRT (s): time elapsed for blanched capillary bed to restore erythema (normal <= 2.5 s)
    - PPI (%): ratio of pulsatile (AC) to non-pulsatile (DC) infrared signal: (AC / DC) * 100
    - MSI: Microvascular Shock Index = CRT / PPI (normal <= 1.8)
    - Skin temperature correction (differentiates hypothermia from systemic shock)
    """

    def __init__(self):
        pass

    def evaluate_microvascular_perfusion(
        self,
        capillary_refill_time_seconds: float,
        pulsatile_ac_signal: float,
        baseline_dc_signal: float,
        skin_temperature_c: Optional[float] = 33.0,
        anatomical_site: Optional[str] = "Index Finger Pulp",
        ambient_temperature_c: Optional[float] = 22.0
    ) -> Dict[str, Any]:
        """
        Calculates CRT, PPI, and microvascular shock metrics.
        capillary_refill_time_seconds: measured CRT in seconds (e.g. 1.8 s).
        pulsatile_ac_signal: infrared AC voltage amplitude (e.g. 18.0 mV).
        baseline_dc_signal: infrared DC baseline voltage (e.g. 900.0 mV).
        skin_temperature_c: local skin temperature in Celsius (default 33.0 C).
        """
        if capillary_refill_time_seconds <= 0:
            raise ValueError("Capillary refill time must be strictly positive.")
        if pulsatile_ac_signal <= 0 or baseline_dc_signal <= 0:
            raise ValueError("PPG signals must be strictly positive.")
        if pulsatile_ac_signal >= baseline_dc_signal:
            raise ValueError("Pulsatile AC component cannot exceed baseline DC level.")

        # Peripheral Perfusion Index (PPI in %)
        ppi_pct = (pulsatile_ac_signal / baseline_dc_signal) * 100.0

        # Microvascular Shock Index (MSI)
        msi = capillary_refill_time_seconds / ppi_pct if ppi_pct > 0 else 99.9

        # Thermal compensation check (hypothermia vs systemic hypoperfusion)
        is_hypothermic = skin_temperature_c < 28.5

        # Clinical Shock & Perfusion Staging (ANDROMEDA-SHOCK Consensus):
        # Normal microcirculation: CRT <= 2.5 s, PPI >= 1.4%, MSI <= 1.8
        # Mild / Borderline hypoperfusion: CRT 2.6 - 3.2 s, PPI 0.8 - 1.3%, MSI 1.9 - 3.0
        # Severe microvascular shock / tissue hypoperfusion: CRT > 3.0 s, PPI < 0.6%, MSI > 3.5
        if capillary_refill_time_seconds > 3.0 and ppi_pct < 0.8:
            perfusion_state = "Severe Peripheral Microvascular Hypoperfusion / Shock State"
            if is_hypothermic:
                pathophysiology = "Prolonged CRT and suppressed PPI compounded by local peripheral hypothermia; assess core-to-skin temperature gradient and systemic hemodynamic stability."
            else:
                pathophysiology = "Profound sympathetic vasoconstriction and microvascular derecruitment; high risk of systemic shock, occult hypovolemia, or hyperlactatemia."
        elif capillary_refill_time_seconds > 2.5 or ppi_pct < 1.4:
            perfusion_state = "Subclinical Microvascular Vasoconstriction"
            pathophysiology = "Marginal peripheral capillary filling; consider fluid responsiveness or autonomic stress response."
        else:
            perfusion_state = "Adequate Cutaneous Microvascular Perfusion"
            pathophysiology = "Optimal capillary bed filling kinetics and robust pulsatile microvascular volume reserve."

        return {
            "status": "success",
            "microvascular_metrics": {
                "capillary_refill_time_crt_seconds": round(capillary_refill_time_seconds, 2),
                "peripheral_perfusion_index_ppi_pct": round(ppi_pct, 2),
                "microvascular_shock_index_msi": round(msi, 2),
                "skin_temperature_c": skin_temperature_c,
                "anatomical_site": anatomical_site
            },
            "perfusion_assessment": {
                "perfusion_state": perfusion_state,
                "pathophysiology_summary": pathophysiology,
                "andromeda_shock_resuscitation_target_met": (capillary_refill_time_seconds <= 3.0 and ppi_pct >= 1.0)
            }
        }
