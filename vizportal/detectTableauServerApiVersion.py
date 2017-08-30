# import all of the modules/packages from login.py

def getSessionInfo(xsrf_token):
    payload = "{\"method\":\"getSessionInfo\",\"params\":{}}"
    endpoint = "getSessionInfo"
    url = tab_server_url + "/vizportal/api/web/v1/"+endpoint
    headers = {
    'content-type': "application/json;charset=UTF-8",
    'accept': "application/json, text/plain, */*",
    'cache-control': "no-cache",
    'X-XSRF-TOKEN':xsrf_token
    }
    SessionResponse = session.post(url, data=payload, headers=headers)
    return SessionResponse

# We need to parse the JSON response from the getSessionInfo call
# and extract the major and minor version numbers

def DetectTableauVersion():
    global xsrf_token
    TabServerSession = getSessionInfo(xsrf_token).text
    TSS = json.loads(TabServerSession)
    v = TSS['result']['server']['version']['externalVersion']
    major = v['major']
    minor = v['minor']
    patch = v['patch']
    tsVersion = major+'.'+minor
    api_version = None

    # Hit this endpoint to access a JSON version of the lookup table above
    # Note: this endpoint is not provided by Tableau and might not be hosted in the future

    api_versions = requests.get('https://tbevdbgwch.execute-api.us-west-2.amazonaws.com/Production/versions/')
    api_lookup = json.loads(api_versions.text)
    for k,v in api_lookup['server'].iteritems():
        if k == tsVersion:
            api_version = v
    return tsVersion, api_version
