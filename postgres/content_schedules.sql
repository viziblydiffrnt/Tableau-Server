select workbook_id, workbook_name, task_id, schedule_id, schedule_type, priority,
day_of_week_mask_array[1] is_sat,
day_of_week_mask_array[2] is_fri,
day_of_week_mask_array[3] is_thu,
day_of_week_mask_array[4] is_wed,
day_of_week_mask_array[5] is_tue,
day_of_week_mask_array[6] is_mon,
day_of_week_mask_array[7] is_sun
from
(
	select *, regexp_split_to_array(day_of_week_mask_binary,'') as day_of_week_mask_array
	from
	(
		select workbook_id, workbook_name, task_id, schedule_id,
		schedule_name, priority,
		case schedule_type
			when 0 then 'Hourly'
			when 1 then 'Daily'
			when 2 then 'Weekly'
			when 3 then 'Monthly' end as schedule_type,
		day_of_week_mask,
		cast(day_of_week_mask::bit(7) as varchar) as day_of_week_mask_binary,
		day_of_month_mask
		from
		(
			select w.id as workbook_id, w.name as workbook_name,
			w.owner_id, w.project_id, w.site_id, t.id as task_id,
			t.schedule_id, t.type, t.luid, s.name as schedule_name,
			s.priority, s.schedule_type, s.day_of_week_mask, s.day_of_month_mask
			from tasks t
			inner join _workbooks w on t.obj_id=w.id
			left join _schedules s on t.schedule_id=s.id
			where w.id = %s
		) a
	) b
) c
