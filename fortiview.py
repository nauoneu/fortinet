import requests
import urllib3
import json
import base64
import os
import time
from pprint import pprint
from datetime import datetime

# global vars
host = '10.130.8.4' #FAZ IP address
user = 'apiuser'
password = 'Fortinet123$'
# daily log rotate at 0:05
logstart = "2021-02-07 00:00:00"
logend = "2021-02-08 00:10:00"
headers = {}
homedir = "./files"
#now = datetime.datetime.now()
#folder = now.strftime('%Y-%m-%d-%H')
folder = 'fazlog'
path = f"{homedir}/{folder}"

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

def runfortiview(sessionid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    headers = {'Content-type': 'application/json'}
    body = {
        "id": "string",
        "jsonrpc": "2.0",
        "method": "add",
        "params": [{
            "apiver": 3,
            "device": [{
                "csfname": '',
                "devid": 'All_FortiGate',
                "devname": ''
            }],
            "filter": "devid",
            "limit": 3,
            "sort-by": [{
                "field": "sessions",
                "order": "asc"
            }],
            "time-range": {
                "end": logend,
                "start": logstart
            },
            "url": f"/fortiview/adom/root/top-sources/run",
        }],
        "session": sessionid
    }

    pprint(body)
    r = requests.post(req_url, json=body, headers=headers, verify=False)
    tid = r.json()
#    pprint(tid)

    return tid['result']['tid']

def getfvresult(tid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    headers = {'Content-type': 'application/json'}
    body = {
        "id": "string",
        "jsonrpc": "2.0",
        "method": "get",
        "params": [{
            "apiver": 3,
            "url": f"/fortiview/adom/root/top-sources/run/{tid}",
        }],
        "session": sessionid
    }

    pprint(body)
    r = requests.post(req_url, json=body, headers=headers, verify=False)
    fvresult = r.json()
    pprint(fvresult)

    return fvresult

if  __name__ == "__main__":
    sessionid = fazlogin()

    tid = runfortiview(sessionid)
    pprint(tid)
    time.sleep(10)
    getfvresult(tid)

    fazlogout(sessionid)
