-- KPI213: % Benchmark Capability Utilization
SELECT (SUM(actual_output) / SUM(benchmark_output)) * 100 AS BenchmarkUtilization
FROM plants;