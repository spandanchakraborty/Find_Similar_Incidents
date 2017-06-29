# poll instance for records and update them based on ML response
import requests
import json
import time

# Set polling interval

pollInterval = 5.0

# Set instance username/password
user = 'frank'
pwd = 'frank1234'

# Set the request parameters
getUrl = 'https://empfyan.service-now.com/api/now/table/u_incident_matching?sysparm_query=u_responded=false'

# Set proper headers
getHeaders = {"Accept": "application/json"}
putHeaders = {"Content-Type": "application/json",
                  "Accept": "application/json"}

def poll():
    # Do the HTTP request
    response = requests.get(getUrl, auth=(user, pwd), headers=getHeaders)

    # Check for HTTP codes other than 200
    if response.status_code == 200:

        responseJson = response.json()

        for i in responseJson["result"]:
            sysID = i["sys_id"]

            # call ml function here and assign return value to responseText
            responseText = "Responded to " + i["u_incident"]
            responseJson = {}
            responseJson["u_response"] = responseText
            responseJson["u_responded"] = "true"
            responseString = json.dumps(responseJson)
            putUrl = 'https://empfyan.service-now.com/api/now/table/u_incident_matching/' + sysID

            update = requests.put(putUrl, auth=(
                user, pwd), headers=putHeaders, data=responseString)

# Execute thread on polling interval
while True:
    poll()
    time.sleep(pollInterval)
