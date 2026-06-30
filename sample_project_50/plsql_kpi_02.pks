-- KPI: Furnace OEE %
CREATE OR REPLACE PACKAGE kpi_furnace AS
  FUNCTION furnace_oee RETURN NUMBER;
END kpi_furnace;
/
-- Body computes (availability * performance * quality) * 100