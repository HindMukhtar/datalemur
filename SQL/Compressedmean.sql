SELECT 
ROUND((sum(item_count*order_occurrences)/sum(order_occurrences))::numeric, 1) as mean
FROM items_per_order;