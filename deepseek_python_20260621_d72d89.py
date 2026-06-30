# ============================================================
# TEST FILE: test_new_kpis.py
# Contains KPIs not yet in the knowledge base
# ============================================================

# KPI: Energy Intensity (BTU/lb)
def calculate_energy_intensity(energy_consumed_btu, production_lbs):
    if production_lbs == 0:
        return 0.0
    return energy_consumed_btu / production_lbs

# KPI: Carbon Footprint (kg CO2/ton)
# Formula: carbon_footprint = (total_emissions_kg / total_production_ton)
def calculate_carbon_footprint(total_emissions_kg, total_production_ton):
    return total_emissions_kg / total_production_ton if total_production_ton else 0.0

# KPI: Water Consumption (gallons/ton)
def calculate_water_consumption(water_used_gallons, production_ton):
    return water_used_gallons / production_ton if production_ton else 0.0

# KPI: Asset Utilization (%)
def calculate_asset_utilization(actual_output, design_capacity):
    return (actual_output / design_capacity) * 100 if design_capacity else 0.0

# KPI: Overall Labor Effectiveness (OLE) (%)
def calculate_ole(available_hours, productive_hours):
    return (productive_hours / available_hours) * 100 if available_hours else 0.0

# KPI: First Pass Yield (%)
def calculate_first_pass_yield(good_units, total_units):
    return (good_units / total_units) * 100 if total_units else 0.0

# KPI: Schedule Adherence (%)
def calculate_schedule_adherence(planned_production, actual_production):
    return (actual_production / planned_production) * 100 if planned_production else 0.0

# KPI: Inventory Turnover (times/year)
def calculate_inventory_turnover(cogs, average_inventory):
    return cogs / average_inventory if average_inventory else 0.0

# KPI: Supplier On-Time Delivery (%)
def calculate_supplier_otd(on_time_deliveries, total_deliveries):
    return (on_time_deliveries / total_deliveries) * 100 if total_deliveries else 0.0

# KPI: Safety Incident Rate (per 200,000 hours)
def calculate_safety_incident_rate(incidents, total_hours_worked):
    return (incidents * 200000) / total_hours_worked if total_hours_worked else 0.0

# KPI: Mean Time To Repair (MTTR) (hours)
# Formula: mttr = total_repair_time / number_of_repairs
def calculate_mttr(total_repair_time_hours, number_of_repairs):
    return total_repair_time_hours / number_of_repairs if number_of_repairs else 0.0

# KPI: Process Capability Index (Cpk)
# Simulated calculation
def calculate_cpk(usl, lsl, mean, std_dev):
    if std_dev == 0:
        return 0.0
    cpu = (usl - mean) / (3 * std_dev)
    cpl = (mean - lsl) / (3 * std_dev)
    return min(cpu, cpl)

# KPI: Overall Cycle Time (hours)
def calculate_overall_cycle_time(total_process_time, number_of_units):
    return total_process_time / number_of_units if number_of_units else 0.0

# KPI: Downtime Percentage (%)
def calculate_downtime_percentage(downtime_hours, total_available_hours):
    return (downtime_hours / total_available_hours) * 100 if total_available_hours else 0.0

# KPI: Reliability (%)
def calculate_reliability(operating_hours, total_hours):
    return (operating_hours / total_hours) * 100 if total_hours else 0.0

# KPI: Quality Yield (%)
def calculate_quality_yield(good_output, total_output):
    return (good_output / total_output) * 100 if total_output else 0.0

# KPI: Scrap Rate (%)
def calculate_scrap_rate(scrap_material, total_material):
    return (scrap_material / total_material) * 100 if total_material else 0.0