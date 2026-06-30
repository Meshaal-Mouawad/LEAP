-- KPI001: % Net Promoter Score (NPS)
SELECT
    (CAST(SUM(CASE WHEN score >= 9 THEN 1 ELSE 0 END) AS FLOAT) -
     CAST(SUM(CASE WHEN score <= 6 THEN 1 ELSE 0 END) AS FLOAT))
    / COUNT(*) * 100 AS NPS
FROM survey_responses;