import azure.functions as func
import logging
import difflib
import json
import urllib.request
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
@app.function_name(name="m365getlist")
@app.route(route="getlist/{datatype}")
@app.blob_input(arg_name="inputblob",
                path="m365list/m365ip_new",
                connection="DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;")
#@app.blob_input(arg_name="inputblob2",
#                path="m365list/m365url_new",
#                connection="DefaultEndpointsProtocol=https;AccountName=tuenothreatfeedlab;AccountKey=3Y6fT2Fsh9uNLVUsexbKlxXpuZueN/c56Bjjm1jhNYRoI5IAwoUa7D7cmjQyOA9oa7u65pRDWD0e+AStMWl1Eg==;EndpointSuffix=core.windows.net")
@app.blob_output(arg_name="outputblob",
                path="m365list/m365ip",
                connection="DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;")
#@app.blob_output(arg_name="outputblob2",
#                path="m365list/m365url",
#                connection="DefaultEndpointsProtocol=https;AccountName=tuenothreatfeedlab;AccountKey=3Y6fT2Fsh9uNLVUsexbKlxXpuZueN/c56Bjjm1jhNYRoI5IAwoUa7D7cmjQyOA9oa7u65pRDWD0e+AStMWl1Eg==;EndpointSuffix=core.windows.net")
#def main(req: func.HttpRequest, inputblob: str, inputblob2: str, outputblob: func.Out[str], outputblob2: func.Out[str]) -> func.HttpResponse:
def main(req: func.HttpRequest, inputblob: str, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info(f'Python Queue trigger function processed {len(inputblob)} bytes')
    outputblob.set(inputblob)

    datatype = req.route_params.get('datatype')
    
    return func.HttpResponse(f"Hello {datatype}! \n")

#    # helper to call the webservice and parse the response
#    def webApiGet(methodName, instanceName, clientRequestId):
#        ws = "https://endpoints.office.com"
#        requestPath = ws + '/' + methodName + '/' + instanceName + '?clientRequestId=' + clientRequestId
#        request = urllib.request.Request(requestPath)
#        with urllib.request.urlopen(request) as response:
#            return json.loads(response.read().decode())
#    
#    clientRequestId = str(uuid.uuid4())
#    endpointSets = webApiGet('endpoints', 'Worldwide', clientRequestId)
#    # filter results for Allow and Optimize endpoints, and transform these into tuples with port and category
#    flatUrls = []
#    for endpointSet in endpointSets:
#        if endpointSet['category'] in ('Optimize', 'Allow', 'Default'):
#            category = endpointSet['category']
#            urls = endpointSet['urls'] if 'urls' in endpointSet else []
#            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
#            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
#            flatUrls.extend([(category, url, tcpPorts, udpPorts) for url in urls])
#    flatIps = []
#    for endpointSet in endpointSets:
#        if endpointSet['category'] in ('Optimize', 'Allow', 'Default'):
#            ips = endpointSet['ips'] if 'ips' in endpointSet else []
#            category = endpointSet['category']
#            # IPv4 strings have dots while IPv6 strings have colons
#            ip4s = [ip for ip in ips if '.' in ip]
#            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
#            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
#            flatIps.extend([(category, ip, tcpPorts, udpPorts) for ip in ip4s])
#
#    reqtype = req.params.get('reqtype')
#    if reqtype == 'ip':
#        return func.HttpResponse('\n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))
#    elif reqtype == 'url':
#        return func.HttpResponse('\n'.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls]))))
