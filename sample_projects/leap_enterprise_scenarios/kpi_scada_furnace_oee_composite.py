# KPI: Furnace OEE Composite
# Description: Combines availability, performance, quality, and furnace energy efficiency into one furnace operating effectiveness score.
# Objective: Give operations leadership a single shift-level view of furnace reliability, production rate, quality acceptance, and energy conversion.
# Formula: (availability_pct / 100) * (performance_pct / 100) * (quality_pct / 100) * (furnace_energy_efficiency_pct / 100) * 100
# Input: availability_pct from DCS runtime counters, performance_pct from production historian rate tags, quality_pct from LIMS release status, and furnace_energy_efficiency_pct from KPI Furnace Energy Efficiency Pct.
# Unit: %
# Data Source: SCADA monitoring historian, DCS runtime counters, LIMS quality release records, and KPI Furnace Energy Efficiency Pct.
# Used In: Executive Reliability Dashboard
# Comments: Synthetic test values: availability_pct=96.8, performance_pct=91.4, quality_pct=98.2, furnace_energy_efficiency_pct=85.97.
def furnace_oee_composite(
    availability_pct: float,
    performance_pct: float,
    quality_pct: float,
    furnace_energy_efficiency_pct: float,
) -> float:
    return (
        (availability_pct / 100)
        * (performance_pct / 100)
        * (quality_pct / 100)
        * (furnace_energy_efficiency_pct / 100)
        * 100
    )
