-- KPI: Polymerization Conversion %
SELECT (converted_mass / NULLIF(feed_mass,0)) * 100 AS [Polymerization Conversion %]
FROM (
  SELECT 980 AS converted_mass, 1000 AS feed_mass
) t;
