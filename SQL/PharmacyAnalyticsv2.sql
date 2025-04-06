SELECT 
manufacturer,
CONCAT('$', CAST(ROUND(SUM(total_sales)/1000000) AS VARCHAR(5)), ' million') as sale
FROM pharmacy_sales
GROUP BY 
manufacturer
ORDER BY 
SUM(total_sales) DESC,
manufacturer;