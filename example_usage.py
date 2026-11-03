"""
Example usage of Cutaneous Capillary Refill Time (CRT) & Peripheral Perfusion Index (PPI).
Demonstrates normal peripheral microcirculation vs septic/hypovolemic shock hypoperfusion.
"""

from client import CapillaryRefillPerfusionClient

def main():
    client = CapillaryRefillPerfusionClient()

    print("=== Case 1: Healthy Cutaneous Microvascular Perfusion ===")
    normal_case = client.evaluate_microvascular_perfusion(
        capillary_refill_time_seconds=1.7,
        pulsatile_ac_signal=22.0,
        baseline_dc_signal=1000.0,
        skin_temperature_c=33.5
    )
    print("Microvascular Perfusion:")
    print(f"  CRT:             {normal_case['microvascular_metrics']['capillary_refill_time_crt_seconds']} s")
    print(f"  PPI:             {normal_case['microvascular_metrics']['peripheral_perfusion_index_ppi_pct']} %")
    print(f"  Shock Index MSI: {normal_case['microvascular_metrics']['microvascular_shock_index_msi']}")
    print(f"  State:           {normal_case['perfusion_assessment']['perfusion_state']}")
    print(f"  Resuscitation Target Met: {normal_case['perfusion_assessment']['andromeda_shock_resuscitation_target_met']}")

    print("\n=== Case 2: Circulatory Shock State (ANDROMEDA-SHOCK Failure) ===")
    shock_case = client.evaluate_microvascular_perfusion(
        capillary_refill_time_seconds=3.8,
        pulsatile_ac_signal=4.5,
        baseline_dc_signal=950.0,
        skin_temperature_c=29.0
    )
    print("Microvascular Perfusion:")
    print(f"  CRT:             {shock_case['microvascular_metrics']['capillary_refill_time_crt_seconds']} s (Severely delayed!)")
    print(f"  PPI:             {shock_case['microvascular_metrics']['peripheral_perfusion_index_ppi_pct']} % (Severe vasoconstriction)")
    print(f"  Shock Index MSI: {shock_case['microvascular_metrics']['microvascular_shock_index_msi']}")
    print(f"  State:           {shock_case['perfusion_assessment']['perfusion_state']}")
    print(f"  Pathophysiology: {shock_case['perfusion_assessment']['pathophysiology_summary']}")

if __name__ == "__main__":
    main()
