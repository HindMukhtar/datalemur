WITH Calls as (SELECT 
policy_holder_id, 
COUNT(case_id) as call_count
FROM callers
GROUP BY 
policy_holder_id) 
SELECT 
COUNT(policy_holder_id) as policy_holder_count
FROM Calls 
WHERE 1=1 
and call_count >=3
;