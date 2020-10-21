import requests
import urllib3
import json
from pprint import pprint

def fmglogin():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ip = "10.130.8.4"
    req_url = 'https://' + ip + '/jsonrpc'
    body = {'id': 1, 'params': [{'url': '/sys/login/user', 'data': {'user': 'apiuser', 'passwd': 'Fortinet123$'}}], 'method': 'exec'}
    r = requests.post(req_url, json=body, verify=False)
    data = r.content
    y = json.loads(data)
#    print(y["session"])
#    return y["session"]
    pprint(y["result"])
    return y["session"]

def fmglogout(sessionid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ip = "10.130.8.4"
    req_url = 'https://' + ip + '/jsonrpc'
    body = {'id': 1, 'params': [{'url': '/sys/logout', 'session': sessionid}], 'method': 'exec'}
    r = requests.post(req_url, json=body, verify=False)
    data = r.content
    y = json.loads(data)
    pprint(y["result"])

def address(sessionid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ip = "10.130.8.4"
    req_url = 'https://' + ip + '/jsonrpc'
    headers = {'Content-type': 'application/json'}
    body = {
        "id": "string",
        "jsonrpc": "2.0",
        "method": "add",
        "params": [{
            "apiver": 3,
            "case-sensitive": false,
            "device": [{
                "csfname": "Corp_SF",
                "devid": "FGT60C0000000001[root]",
                "devname": "FGT-vancouver[traffic]"
            }],
            "filter": "",
            "logtype": "traffic",
            "time-order": "desc",
            "time-range": {
                "end": "2019-07-03T17:16:35",
                "start": "2019-07-02T17:16:35"
            },
            "url": "/logview/adom/root/logsearch"
        }],
        "session": sessionid
    }
    r = requests.post(req_url, json=body, headers=headers, verify=False)
    data = r.content
    y = json.loads(data)
    pprint(y["result"])

if  __name__ == "__main__":
    sessionid = fmglogin()
#    address(sessionid)
    fmglogout(sessionid)
