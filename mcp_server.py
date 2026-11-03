"""
MCP Server for Cutaneous Capillary Refill Time (CRT) & Peripheral Perfusion Index (PPI).
Exposes tools for microvascular perfusion, shock triage, and peripheral vascular monitoring.
"""

import json
from typing import Dict, Any, Optional
from client import CapillaryRefillPerfusionClient


def handle_evaluate_microvascular(params: Dict[str, Any]) -> Dict[str, Any]:
    capillary_refill_time_seconds = float(params.get("capillary_refill_time_seconds", 1.8))
    pulsatile_ac_signal = float(params.get("pulsatile_ac_signal", 18.0))
    baseline_dc_signal = float(params.get("baseline_dc_signal", 900.0))
    skin_temperature_c = float(params.get("skin_temperature_c", 33.0))
    anatomical_site = str(params.get("anatomical_site", "Index Finger Pulp"))
    ambient_temperature_c = float(params.get("ambient_temperature_c", 22.0))

    client = CapillaryRefillPerfusionClient()
    return client.evaluate_microvascular_perfusion(
        capillary_refill_time_seconds=capillary_refill_time_seconds,
        pulsatile_ac_signal=pulsatile_ac_signal,
        baseline_dc_signal=baseline_dc_signal,
        skin_temperature_c=skin_temperature_c,
        anatomical_site=anatomical_site,
        ambient_temperature_c=ambient_temperature_c
    )


TOOLS = {
    "evaluate_microvascular_perfusion": {
        "description": "Calculates Capillary Refill Time (CRT in seconds), Peripheral Perfusion Index (PPI = AC/DC * 100), and Microvascular Shock Index (MSI = CRT / PPI) for shock triage.",
        "parameters": {
            "type": "object",
            "properties": {
                "capillary_refill_time_seconds": {
                    "type": "number",
                    "description": "Time in seconds for blanched capillary bed to restore normal color (e.g. 1.8 s)."
                },
                "pulsatile_ac_signal": {
                    "type": "number",
                    "description": "Pulsatile infrared PPG AC voltage in mV (e.g. 18.0 mV)."
                },
                "baseline_dc_signal": {
                    "type": "number",
                    "description": "Non-pulsatile baseline infrared PPG DC voltage in mV (e.g. 900.0 mV)."
                },
                "skin_temperature_c": {
                    "type": "number",
                    "description": "Local skin surface temperature in Celsius, default 33.0 C."
                },
                "anatomical_site": {
                    "type": "string",
                    "description": "Measurement site ('Index Finger Pulp' or 'Knee'), default 'Index Finger Pulp'."
                },
                "ambient_temperature_c": {
                    "type": "number",
                    "description": "Ambient room temperature in Celsius, default 22.0 C."
                }
            },
            "required": ["capillary_refill_time_seconds", "pulsatile_ac_signal", "baseline_dc_signal"]
        },
        "handler": handle_evaluate_microvascular
    }
}


def process_request(request_str: str) -> str:
    try:
        req = json.loads(request_str)
        method = req.get("method")
        req_id = req.get("id")

        if method == "tools/list":
            tools_list = [
                {
                    "name": name,
                    "description": spec["description"],
                    "inputSchema": spec["parameters"]
                }
                for name, spec in TOOLS.items()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name not in TOOLS:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                })

            result = TOOLS[tool_name]["handler"](args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            })

        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": f"Unsupported method '{method}'"}
            })

    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        if line.strip():
            print(process_request(line))
            sys.stdout.flush()
