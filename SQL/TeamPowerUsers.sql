-- use CTE number of count of user messages in august 
WITH counts as (SELECT 
count(message_id) as message_count
, sender_id
FROM messages
WHERE sent_date between '2022-08-01' and '2022-08-31'
GROUP BY 
sender_id) 

-- select top 2 users with highest number of messages 
SELECT sender_id, message_count FROM counts ORDER BY message_count DESC LIMIT 2
;