-- KPI: Furnace OEE %
CREATE OR REPLACE PACKAGE BODY kpi_furnace AS
  FUNCTION furnace_oee RETURN NUMBER IS
    availability NUMBER := 0.92;
    performance  NUMBER := 0.95;
    quality      NUMBER := 0.98;
    oee          NUMBER;
  BEGIN
    oee := (availability * performance * quality) * 100;
    RETURN oee;
  END furnace_oee;
END kpi_furnace;
/
