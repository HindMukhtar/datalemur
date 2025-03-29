-- Using a subquery, create a skills flag if skill includes python, tabluau or postgresSQL 
-- Sum all flags bt candidate 
-- if sum of skill_flag >=3, then candidate has all 3 skills 

SELECT candidate_id FROM 
(
SELECT 
candidate_id
, sum(CASE 
  WHEN skill in ('Python', 'Tableau', 'PostgreSQL') 
  THEN 1 ELSE 0 END) AS skill_flag
FROM candidates c
GROUP BY 
candidate_id) as t 
WHERE skill_flag >= 3
