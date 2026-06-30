KPI Discovery Report
====================

Scan Overview
-------------

.. list-table::
   :header-rows: 0
   :widths: 35 65

   * - Source folder
     - ``/Users/meshaalmouawad/Downloads/AIkpi/sample_project``
   * - All filesystem items found
     - 14
   * - All filesystem files found
     - 14
   * - All filesystem directories found
     - 0
   * - Files after directory exclusions
     - 14
   * - Source files selected for KPI scan
     - 13
   * - Binary/image files skipped
     - 0
   * - Unsupported files skipped
     - 0
   * - Non-KPI candidates filtered
     - 1
   * - Ignored files skipped
     - 1
   * - Ignored directories skipped
     - 0
   * - Lines analyzed
     - 108
   * - KPIs detected
     - 12
   * - Compliance detail phase wall time
     - 0.01s

Confidence Summary
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Band
     - Count
     - Meaning
   * - High
     - 12
     - Explicit KPI marker, measure, or strong domain pattern
   * - Medium
     - 0
     - Useful candidate; review formula/context
   * - Low
     - 0
     - Weak candidate; manual validation recommended

Languages Detected
------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Language
     - KPI Count
   * - csharp
     - 2
   * - abap
     - 1
   * - dax
     - 1
   * - generic
     - 1
   * - hana
     - 1
   * - iec_st
     - 1
   * - plsql
     - 1
   * - python
     - 1
   * - sql
     - 1
   * - tsql
     - 1
   * - vbnet
     - 1

Detection Methods
-----------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Method
     - KPI Count
   * - Comment
     - 7
   * - Sql Comment
     - 3
   * - Dax Measure
     - 1
   * - Hana Json
     - 1

Governance Summary
------------------

.. list-table:: Assignment Method
   :header-rows: 1
   :widths: 60 40

   * - Method
     - KPI Count
   * - Rule-based inference
     - 12

.. list-table:: Accountable Owner
   :header-rows: 1
   :widths: 60 40

   * - Accountable Owner
     - KPI Count
   * - Enterprise Data Owner
     - 4
   * - Operations Data Owner
     - 3
   * - Finance Data Owner
     - 2
   * - HSE Data Owner
     - 2
   * - Maintenance Data Owner
     - 1

Possible Duplicate KPI Names
----------------------------

No duplicate KPI names were detected.


KPI Inventory
-------------

.. list-table::
   :header-rows: 1
   :widths: 24 10 10 18 18 20

   * - KPI
     - Confidence
     - Language
     - Detection
     - Accountable
     - Source
   * - :doc:`yield_percentage`
     - 95%
     - PLSQL
     - Sql Comment
     - Operations Data Owner
     - ``plsql_kpi.pks``
   * - :doc:`maintenance_to_operating_cost_ratio`
     - 90%
     - GENERIC
     - Comment
     - Finance Data Owner
     - ``generic_kpi.txt``
   * - :doc:`kpi_flare_recovery_pct`
     - 85%
     - HANA
     - Hana Json
     - HSE Data Owner
     - ``ana_kpi.hdbview``
   * - :doc:`propylene_to_ethylene_pe_ratio`
     - 90%
     - CSHARP
     - Comment
     - Enterprise Data Owner
     - ``dotnet_kpi.cs``
   * - :doc:`polymer_melt_flow_index_mfi_variance`
     - 90%
     - ABAP
     - Comment
     - Enterprise Data Owner
     - ``abap_kpi.abap``
   * - :doc:`cooling_water_deltat_c`
     - 90%
     - CSHARP
     - Comment
     - Enterprise Data Owner
     - ``csv_kpi.cs``
   * - :doc:`onspec_rate`
     - 95%
     - SQL
     - Sql Comment
     - Enterprise Data Owner
     - ``sql_kpi.sql``
   * - :doc:`mean_time_between_failures_mtbf`
     - 90%
     - VBNET
     - Comment
     - Maintenance Data Owner
     - ``vb_kpi.vb``
   * - :doc:`sox_emissions_concentration_kgm3`
     - 90%
     - IEC_ST
     - Comment
     - HSE Data Owner
     - ``lc_kpi.st``
   * - :doc:`daily_feedstock_throughput_tonsday`
     - 90%
     - PYTHON
     - Comment
     - Operations Data Owner
     - ``python_kpi.py``
   * - :doc:`oee`
     - 95%
     - DAX
     - Dax Measure
     - Operations Data Owner
     - ``ax_kpi.dax``
   * - :doc:`specific_catalyst_cost_ton`
     - 95%
     - TSQL
     - Sql Comment
     - Finance Data Owner
     - ``tsql_kpi.tsql``
