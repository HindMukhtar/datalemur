-- get app click through rate in 2022 
-- CTR = 100*clicks/impressions
SELECT 
ROUND(100.0*(SUM(1.0) FILTER (WHERE event_type = 'click')/SUM(1.0) FILTER (WHERE event_type = 'impression')), 2) as CTR,
app_id
FROM events
WHERE
timestamp between '2022-01-01' and '2022-12-31'
GROUP BY 
app_id