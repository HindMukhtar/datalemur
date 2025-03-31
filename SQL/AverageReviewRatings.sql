SELECT 
EXTRACT('month' from submit_date::date) as mth, 
product_id as product, 
ROUND(avg(stars), 2) as avg_rating
FROM reviews
GROUP BY 
EXTRACT('month' from submit_date::date), 
product_id
ORDER BY 
EXTRACT('month' from submit_date::date), 
product_id;