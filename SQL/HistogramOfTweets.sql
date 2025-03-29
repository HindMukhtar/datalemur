-- Use a subquery to get tweet counts by user for the year 2022 
-- Group by users to create histogram 
SELECT 
tweet_count as tweet_bucket
,COUNT(user_id) as users_num
FROM(
SELECT 
count(tweet_id) as tweet_count
,user_id
FROM tweets
WHERE tweet_date >= '2022-01-01' and tweet_date <= '2022-12-31'
GROUP BY
user_id) AS t 
GROUP BY 
tweet_count