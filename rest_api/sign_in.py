def sign_in(name, password, site=""):
    global token
    url = tab_server_url + "api/%s/auth/signin" % (api_version)

    #Build the request
    xml_payload_for_request = ET.Element('tsRequest')
    credentials_element = ET.SubElement(xml_payload_for_request,'credentials',name=name, password=password)
    site_element = ET.SubElement(credentials_element, 'site', contentUrl=site)
    xml_payload_for_request = ET.tostring(xml_payload_for_request)

    #Sign in to Tableau Server
    server_response = requests.post(url, data=xml_payload_for_request)
    if server_response.status_code != 200:
        print "Problem signing into Tableau Server: %s" % (server_response.text)
    else:
        print "Sign in to Tableau Server: %s" % (url)

    xml_response = ET.fromstring(server_response.text)

    #Retrieve the token and Site ID (we'll need these for the subsequent API calls)
    token = xml_response.find('t:credentials', namespaces=xmlns).attrib.get('token')
    site_id = xml_response.find('.//t:site', namespaces=xmlns).attrib.get('id')
    user_id = xml_response.find('.//t:user', namespaces=xmlns).attrib.get('id')

    print "Sign in to Tableau Server successful!\n"
    print "token = "+token, "site_id = "+site_id, "user_id = "+user_id+"\n"
    return token, site_id, user_id
