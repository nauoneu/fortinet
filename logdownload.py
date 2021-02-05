import requests
import urllib3
import json
from pprint import pprint

# global vars
host = '10.130.8.4' #FAZ IP address
user = 'apiuser'
password = 'Fortinet123$'
logstart = "2021-02-04 00:00:00"
logend = "2021-02-05 00:00:00"
devid = 'All_FortiGate'
logtype = 'virus'
headers = {}

def fazlogin():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    body = {'id': 1, 'params': [{'url': '/sys/login/user', 'data': {'user': user, 'passwd': password}}], 'method': 'exec'}
    r = requests.post(req_url, json=body, verify=False)
    data = r.json()
#    pprint(data["result"])
    return data["session"]

def fazlogout(sessionid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    body = {'id': 1, 'params': [{'url': '/sys/logout', 'session': sessionid}], 'method': 'exec'}
    r = requests.post(req_url, json=body, verify=False)
    data = r.json()
#    pprint(data["result"])

"""
def logsearchreq(sessionid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    headers = {'Content-type': 'application/json'}
    body = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "add",
        "params": [{
            "apiver": 3,
            "device": [{
                "devid": devid
            }],
            "filter": "",
            "logtype": logtype,
            "time-order": "desc",
            "time-range": {
                "start": logstart,
                "end": logend
            },
            "url": "/logview/adom/root/logsearch"
        }],
        "session": sessionid
    }

    try:
#        pprint(body)
        r = requests.post(req_url, json=body, headers=headers, verify=False)
        data = r.json()
#        pprint(data['result']['tid'])
        tid = data['result']['tid']
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return
    
    return tid
"""

def getfilelist(sessionid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    headers = {'Content-type': 'application/json'}
    body = {
        "id": "string",
        "jsonrpc": "2.0",
        "method": "get",
        "params": [{
            "apiver": 3,
            "devid": "FG3H1E5818901626",
            "filename": "",
            "time-range": {
                "start": logstart,
                "end": logend
            },
#            "limit": 50,
#            "offset": 0,
            "url": f"/logview/adom/root/logfiles/state",
            "vdom": ""
        }],
        "session": sessionid
    }

    try:
#        pprint(body)
        r = requests.post(req_url, json=body, headers=headers, verify=False)
        data = r.json()
#        pprint(data)
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return
    
    return data

if  __name__ == "__main__":
    sessionid = fazlogin()
    logdata = getfilelist(sessionid)
    pprint(logdata)
    fazlogout(sessionid)
