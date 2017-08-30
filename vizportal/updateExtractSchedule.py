# import all of the modules/packages from login.py

def updateExtractSchedule(task_id, schedule_id, xsrf_token):
     payload = "{\"method\":\"setExtractTasksSchedule\",\"params\":{\"ids\":[\"%s\"], \"scheduleId\":\"%s\"}}" % (task_id, schedule_id)
     endpoint = "setExtractTasksSchedule"
     url = tab_server_url + "/vizportal/api/web/v1/"+endpoint
     headers = {
     'content-type': "application/json;charset=UTF-8",
     'accept': "application/json, text/plain, */*",
     'cache-control': "no-cache",
     'X-XSRF-TOKEN':xsrf_token
      }
     response = session.post(url, data=payload, headers=headers)
     print response.status_code
     return response
