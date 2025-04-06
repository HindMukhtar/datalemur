WITH profit as (SELECT 
manufacturer, 
drug, 
sum(total_sales) - sum(cogs) as profit
FROM pharmacy_sales
GROUP BY 
manufacturer, 
drug)
SELECT 
manufacturer,
COUNT(drug) as drug_count,
ABS(SUM(profit)) as total_loss
from profit 
WHERE 1=1 
AND profit < 0
GROUP BY 
manufacturer
ORDER BY 
total_loss DESC
;