# file: kpi_broken_utilization.py


def calculate_utilization(
    actual_production_time, planned_operation_time, maintenance_time
):
    """
    WRONG KPI: includes maintenance in production time
    Should trigger governance conflict
    """
    return (actual_production_time + maintenance_time) / planned_operation_time
