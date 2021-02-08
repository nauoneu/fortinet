import requests
import json
import http
import http.cookiejar
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url_login = "https://10.130.8.102/logincheck"
client = requests.session()

#Loginrequest
payload = "username=admin&secretkey=fortinet"
r = client.post(url_login, data=payload, verify=False)

apscookie = r.cookies
for cookie in client.cookies:
    if cookie.name == 'ccsrftoken':
        csrftoken = cookie.value[1:-1] #token stored as a list

client.headers.update({'X-CSRFTOKEN': csrftoken})
print(csrftoken)
