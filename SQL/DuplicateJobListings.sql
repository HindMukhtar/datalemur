WITH jobcounts as (SELECT 
  company_id,
  count(job_id) as job_count
FROM job_listings
GROUP BY
company_id, 
title, 
description) 

SELECT
COUNT(company_id) as duplicate_companies
FROM jobcounts 
WHERE job_count > 1
;