select id, name, workbook_url, owner_id, project_id, site_id, site_luid, luid, date_part('day',now()-last_view_time) as days_since_last_view
from
(
	select w.id, w.name, w.workbook_url, w.owner_id, w.project_id, w.site_id, wkb.luid, sites.luid as site_luid, max(vs.last_view_time) as last_view_time
	from _workbooks w
	left join _users u on w.owner_id=u.id
	left join _views_stats vs on w.id=vs.views_workbook_id
	join workbooks wkb on w.id=wkb.id
	join sites on sites.id=w.site_id
	where date_part('day',now()-last_view_time) >= %s
	group by w.id, w.name, w.workbook_url, w.owner_id, w.project_id, w.site_id, wkb.luid, site.luid
) a
