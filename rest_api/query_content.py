def query_content(content_type, site_id, content_luid):
    """
    Queries the server for a specific piece of content.

    'content_type'  is the type of content to be queried. Acceptable values are 'workbook' and 'datasource'.
    'site_id'       is the ID (as a string) of the site on the server where the content is located. Use the value retrieved from sign_in()
    'content_luid'  is the ID (as a string) of the content on the server to to be queried.
                    Note that this is not the same as the workbook_id or datasource_id found in the Postgres database.
                    It is the unique id or luid value.

    Returns the name of the content and its owner_id (as a string).
    """
    headers = {'x-tableau-auth':token}

    # Configure call for querying Workbook
    if content_type == 'workbook':
        workbook_url = tab_server_url + "/api/%s/sites/%s/workbooks/%s" % (api_version,site_id,content_luid)
        content_response = requests.get(workbook_url, headers=headers)
        if content_response.status_code != 200:
            print content_response.text

        xml_response = ET.fromstring(_encode_for_display(content_response.text))

        workbook_name = xml_response.find('.//t:workbook', namespaces=xmlns).attrib.get('name')
        workbook_owner_id = xml_response.find('.//t:owner', namespaces=xmlns).attrib.get('id')

        tags = xml_response.findall('.//t:tag', namespaces=xmlns)
        workbook_tags = []
        for t in tags:
            workbook_tags.append(t.attrib.get('label'))

        print "Workbook name = %s and is owned by %s" % (workbook_name, workbook_owner_id)
        return workbook_name, workbook_owner_id, workbook_tags

    # Configure call for querying Datasource
    elif content_type == 'datasource':
        datasource_url = tab_server_url + "/api/%s/sites/%s/datasources/%s" % (api_version,site_id,content_luid)
        content_response = requests.get(datasource_url, headers=headers)
        if content_response.status_code != 200:
            print content_response.text
        xml_response = ET.fromstring(_encode_for_display(content_response.text))

        datasource_name = xml_response.find('.//t:datasource', namespaces=xmlns).attrib.get('name')
        datasource_owner_id = xml_response.find('.//t:owner', namespaces=xmlns).attrib.get('id')

        tags = xml_response.findall('.//t:tag', namespaces=xmlns)
        datasource_tags = []
        for t in tags:
            datasource_tags.append(t.attrib.get('label'))

        print "Datasource name = %s and is owned by %s" % (datasource_name, datasource_owner_id)
        return datasource_name, datasource_owner_id, datasource_tags
