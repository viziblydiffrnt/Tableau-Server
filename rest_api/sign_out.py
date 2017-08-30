def sign_out():
    global token
    url = tab_server_url + "/api/%s/auth/signout" % (api_version)
    headers = {'x-tableau-auth':token}
    server_response = requests.post(url, headers=headers)
    token = None
    if server_response.status_code != 200:
        print server_response.text
    else:
        print "Signed out of Tableau Server successfully.\n"
    return
