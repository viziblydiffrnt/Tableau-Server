select id, luid, name,
case schedule_type
	when 0 then 'Hourly'
	when 1 then 'Daily'
	when 2 then 'Weekly'
	when 3 then 'Monthly' end as schedule_type
from schedules
