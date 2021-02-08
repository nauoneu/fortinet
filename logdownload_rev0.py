import requests
import urllib3
import json
from pprint import pprint
from datetime import datetime

# global vars
host = '10.130.8.4' #FAZ IP address
user = 'apiuser'
password = 'Fortinet123$'
logstart = "2021-02-04 00:00:00"
logend = "2021-02-05 00:00:00"
#devid = 'All_FortiGate'
devid = ''
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
#            "devid": devid,
#            "filename": "",
            "devid": "FG5H1E5818903582",
            "filename": "tlog.1555569529.log.gz",
            "time-range": {
                "end": logend,
                "start": logstart
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
    filelist = getfilelist(sessionid)
    pprint(filelist)
    devlist = filelist['result']['device-file-list']
    for i, j in enumerate(devlist):
        files = j['vdom-file-list'][0]['logfile-list']['tlog']['files']
        for k, l in enumerate(files):
            filename = l['filename']
            starttime = datetime.strptime(l['starttime'], '%Y-%m-%d %H:%M:%S')
            endtime = datetime.strptime(l['endtime'], '%Y-%m-%d %H:%M:%S')
            logstartdt = datetime.strptime(logstart, '%Y-%m-%d %H:%M:%S')
            logenddt = datetime.strptime(logend, '%Y-%m-%d %H:%M:%S')
#            if (logstartdt < starttime) and (logenddt > endtime):
            if (logstartdt > starttime) and (logenddt > endtime):
                print('{0}:{1}'.format(k, l))

    fazlogout(sessionid)
