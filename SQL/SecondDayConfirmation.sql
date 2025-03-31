-- Get user IDs of user that confirm their email the day after signing up 
SELECT 
  e.user_id
FROM emails e
JOIN texts t 
on t.email_id = e.email_id
AND t.signup_action = 'Confirmed'
AND (t.action_date::date - e.signup_date::date) = 1;