-- KPI: Reactor Selectivity %
CREATE OR REPLACE PACKAGE kpi_pkg AS
  FUNCTION reactor_selectivity RETURN NUMBER;
END kpi_pkg;
/
-- Body hint: (desired / total) * 100