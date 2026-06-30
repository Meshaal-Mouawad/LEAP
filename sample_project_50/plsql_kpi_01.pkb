-- KPI: Reactor Selectivity %
CREATE OR REPLACE PACKAGE BODY kpi_pkg AS
  FUNCTION reactor_selectivity RETURN NUMBER IS
    desired NUMBER := 910;
    total   NUMBER := 1000;
    res     NUMBER;
  BEGIN
    res := (desired / NULLIF(total,0)) * 100;
    RETURN res;
  END reactor_selectivity;
END kpi_pkg;
/
