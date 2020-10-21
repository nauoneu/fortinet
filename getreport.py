import requests
import urllib3
import json
from pprint import pprint

# global vars
host = '10.130.8.4' #FAZ IP address
user = 'apiuser'
password = 'Fortinet123$'
fromdate  = "2020-10-01 00:00:00"
todate = "2020-10-21 00:00:00"
headers = {}

def fmglogin():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    body = {'id': 1, 'params': [{'url': '/sys/login/user', 'data': {'user': user, 'passwd': password}}], 'method': 'exec'}
    r = requests.post(req_url, json=body, verify=False)
    data = r.json()
#    pprint(data["result"])
    return data["session"]

def fmglogout(sessionid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    body = {'id': 1, 'params': [{'url': '/sys/logout', 'session': sessionid}], 'method': 'exec'}
    r = requests.post(req_url, json=body, verify=False)
    data = r.json()
#    pprint(data["result"])

def reportsearch(sessionid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    headers = {'Content-type': 'application/json'}
    body = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "get",
        "params": [{
            "apiver": 3,
            "sort-by": [{
                "field": "",
                "order": "asc"
            }],
            "state": "generated",
            "time-range": {
                "end": todate,
                "start": fromdate
            },
            "url": "/report/adom/root/reports/state"
        }],
        "session": sessionid
    }

    try:
#        pprint(body)
        r = requests.post(req_url, json=body, headers=headers, verify=False)
        data = r.json()
        total = int(data['result']['count'])
        tidlist = {}
        for i in range(total):
            tidlist[i] = data['result']['data'][i]['tid']

    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return
    
    return tidlist

def getreport(sessionid, i, tid):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req_url = 'https://' + host + '/jsonrpc'
    headers = {'Content-type': 'application/json'}
    body = {
        "id": i,
        "jsonrpc": "2.0",
        "method": "get",
        "params": [{
            "apiver": 3,
            "data-type": "text",
            "format": "csv",
            "url": f"/report/adom/root/reports/data/{tid}"
        }],
        "session": sessionid
    }
#    pprint(body)

    try:
        r = requests.post(req_url, json=body, headers=headers, verify=False)
        data = r.json()
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return

    return data

if  __name__ == "__main__":
    sessionid = fmglogin()

    tidlist = reportsearch(sessionid)
#    pprint(tidlist)

    for i in tidlist:
        tid = tidlist[i]
        reportdata = getreport(sessionid, i, tid)
        pprint(reportdata)

    fmglogout(sessionid)
