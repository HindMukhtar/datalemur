-- use CTE to get all managers from table 

WITH managers as (
  SELECT 
    employee_id, 
    salary, 
    department_id
FROM employee
WHERE 1=1 
AND employee_id in (SELECT DISTINCT manager_id from employee))

-- Join employee table on managers table and filter where employee earns more than manager 
SELECT 
e.employee_id , 
e.name
FROM employee e
JOIN managers m 
ON m.employee_id = e.manager_id
AND e.salary > m.salary

