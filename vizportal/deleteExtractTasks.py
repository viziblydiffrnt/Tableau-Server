# import all of the modules/packages from login.py

def deleteExtractTasks(task_id, xsrf_token):
    payload = "{\"method\":\"deleteExtractTasks\",\"params\":{\"ids\":[\"%s\"]}}" % (task_id)
    endpoint = "deleteExtractTasks"
    url = tab_server_url + "/vizportal/api/web/v1/"+endpoint
    headers = {
    'content-type': "application/json;charset=UTF-8",
    'accept': "application/json, text/plain, */*",
    'cache-control': "no-cache",
    'X-XSRF-TOKEN':xsrf_token
    response = session.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        print "Failed to delete extract schedule"
    else:
        print "Extract schedule successfully removed"
    return response
