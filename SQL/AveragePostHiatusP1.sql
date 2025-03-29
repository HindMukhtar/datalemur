-- use CTE to get users first and last post within the year 2021 
WITH twice as (
SELECT 
count(post_id) as post_count
, MIN(post_date) as first_post
, MAX(post_date) as last_post
, user_id 
FROM posts
WHERE post_date between '2021-01-01' and '2021-12-31'
GROUP BY 
user_id) 

-- count days between the first and last post 
SELECT 
user_id 
, (last_post::date - first_post::date) as days_between
FROM twice 
WHERE post_count >= 2 

