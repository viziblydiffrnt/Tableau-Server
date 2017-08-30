def query_schedules():
    global server_schedules
    headers = {'x-tableau-auth':token}
    schedule_url  = tab_server_url + "/api/%s/schedules" % (api_version)
    response = requests.get(schedule_url, headers=headers)
    if response.status_code != 200:
        print response.text

    xml_response = ET.fromstring(_encode_for_display(response.text))
    server_schedules = []

    schedules = xml_response.findall('.//t:schedule', namespaces=xmlns)
    for s in schedules:
        schedule_luid = s.attrib.get('id')
        schedule_name = s.attrib.get('name')
        schedule_state = s.attrib.get('state')
        schedule_frequency = s.attrib.get('frequency')
        schedule_type = s.attrib.get('type')
        schedule_details = {'schedule_luid':schedule_luid, 'schedule_name':schedule_name, 'state':schedule_state, 'frequency':schedule_frequency, 'type':schedule_type}
        server_schedules.append(schedule_details)

    return server_schedules
