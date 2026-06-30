-- KPI: Propylene Yield %
SELECT 100.0 * (produced_mass / NULLIF(feed_mass,0)) AS [Propylene Yield %]
FROM (
  SELECT 4500 AS produced_mass, 5200 AS feed_mass
) t;
-- Formula: (produced_mass / feed_mass) * 100