-- use CTE to number of likes by page 
WITH likes as (
SELECT 
COUNT(user_id) num_likes
, page_id 
FROM page_likes 
GROUP BY 
page_id) 


-- join with pages table to get page where there are no likes 
SELECT 
p.page_id
FROM pages p 
LEFT JOIN likes as l 
ON p.page_id = l.page_id 
WHERE num_likes is NULL 