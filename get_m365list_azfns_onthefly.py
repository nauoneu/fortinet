import azure.functions as func
import logging
import difflib
import json
import urllib.request
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger_test")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # helper to call the webservice and parse the response
    def webApiGet(methodName, instanceName, clientRequestId):
        ws = "https://endpoints.office.com"
        requestPath = ws + '/' + methodName + '/' + instanceName + '?clientRequestId=' + clientRequestId
        request = urllib.request.Request(requestPath)
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    
    clientRequestId = str(uuid.uuid4())
    endpointSets = webApiGet('endpoints', 'Worldwide', clientRequestId)
    # filter results for Allow and Optimize endpoints, and transform these into tuples with port and category
    flatUrls = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow', 'Default'):
            category = endpointSet['category']
            urls = endpointSet['urls'] if 'urls' in endpointSet else []
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatUrls.extend([(category, url, tcpPorts, udpPorts) for url in urls])
    flatIps = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow', 'Default'):
            ips = endpointSet['ips'] if 'ips' in endpointSet else []
            category = endpointSet['category']
            # IPv4 strings have dots while IPv6 strings have colons
            ip4s = [ip for ip in ips if '.' in ip]
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatIps.extend([(category, ip, tcpPorts, udpPorts) for ip in ip4s])

    reqtype = req.params.get('reqtype')
    if reqtype == 'ip':
        return func.HttpResponse('\n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))
    elif reqtype == 'url':
        return func.HttpResponse('\n'.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls]))))
