select
	su.friendly_name as user_friendly_name,
	su.name as system_user_name,
	su.email,
	u2.licensing_role_name,
	u2.site_id,
	u.luid as user_luid
from system_users su
join users u on su.id=u.system_user_id
join _user u2 on u.id=u2.id
where u.id = %s
