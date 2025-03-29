-- select parts where date is still null 
SELECT 
part,
assembly_step
FROM parts_assembly where finish_date is null;