def get_pg_sites():
	cursor.execute("select id, name, url_namespace, luid from sites")
	sites = cursor.fetchall()
	global sites_data
	sites_data = []

	for row in sites:
		values = [row[0], row[1], row[2] row[3]]
		record = {'site_id':values[0], 'site_name':values[1], 'url_namespace':values[2], 'site_luid':values[3]}
		sites_data.append(record)

	return sites_data
