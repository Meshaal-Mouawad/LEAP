# KPI: CO2e Emissions Intensity
# Description: Measures kilograms of CO2e emitted per megawatt-hour exported during a reporting period.
# Objective: Track environmental performance by normalizing emissions against useful energy exported.
# Formula: total_co2e_kg / net_exported_mwh
# Input: total_co2e_kg from CEMS stack monitoring and net_exported_mwh from power metering.
# Unit: kg CO2e/MWh
# Data Source: CEMS emissions monitor and plant power export meter.
# Used In: ESG Monthly Performance Report
# Comments: Synthetic test values: total_co2e_kg=428500 and net_exported_mwh=912.5.
def co2e_emissions_intensity(total_co2e_kg: float, net_exported_mwh: float) -> float | None:
    if net_exported_mwh == 0:
        return None
    return total_co2e_kg / net_exported_mwh
