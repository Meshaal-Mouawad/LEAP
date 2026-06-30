# KPI: Furnace Energy Efficiency Pct
# Description: Measures the percentage of fuel energy converted into useful furnace heat during a production shift.
# Objective: Detect thermal energy loss from burner fouling, poor air-fuel ratio, or heat-transfer degradation before yield is affected.
# Formula: (useful_heat_mmbtu / fuel_gas_mmbtu) * 100
# Input: useful_heat_mmbtu from SCADA tag FURNACE_101.USEFUL_HEAT_MMBTU and fuel_gas_mmbtu from SCADA tag FURNACE_101.FUEL_GAS_MMBTU.
# Unit: %
# Data Source: SCADA monitoring historian via OPC tags FURNACE_101.USEFUL_HEAT_MMBTU and FURNACE_101.FUEL_GAS_MMBTU.
# Used In: Furnace OEE Composite
# Comments: Synthetic test values: useful_heat_mmbtu=812.4 and fuel_gas_mmbtu=945.0 for shift 2026-06-20-A.
def furnace_energy_efficiency_pct(useful_heat_mmbtu: float, fuel_gas_mmbtu: float) -> float | None:
    if fuel_gas_mmbtu == 0:
        return None
    return (useful_heat_mmbtu / fuel_gas_mmbtu) * 100
