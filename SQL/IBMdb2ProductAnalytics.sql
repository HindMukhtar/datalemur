WITH qs AS (SELECT 
coalesce(COUNT(DISTINCT q.query_id), 0) as unique_queries, 
e.employee_id
FROM employees e
LEFT JOIN queries q
on e.employee_id = q.employee_id
AND query_starttime >= '2023-07-01'
AND query_starttime <= '2023-10-01'
GROUP BY 
e.employee_id)
SELECT 
unique_queries,
COUNT(employee_id) as employee_count
FROM qs
GROUP BY 
unique_queries
ORDER BY 
unique_queries;
