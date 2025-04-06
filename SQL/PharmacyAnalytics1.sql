SELECT 
drug, 
sum(total_sales) - sum(cogs) as total_profit
FROM pharmacy_sales
GROUP BY 
drug
ORDER BY 
sum(total_sales) - sum(cogs) DESC
LIMIT 3;