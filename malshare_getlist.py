#! /usr/bin/env python
# Download files with given hashes.json file

import requests
import argparse
import json
import logging
import os
import datetime
import sys
from pprint import pprint

# global vars
api_key = "14b204a8ff4fdc3e6f0a7a0aee38446eb2d560c10d76bae2e8980043d5d628af"
url = "https://malshare.com/api.php"
getlist = {'action': 'getlist', 'api_key': api_key}
now = datetime.datetime.now()
folder = now.strftime('%Y-%m-%d-%H')
#folder = f"{now.year}-{now.month}-{now.day}-{now.hour}"
path = f"/var/www/html/files/{folder}"

def download_hashlist():
    try:
        r = requests.get(url, params = getlist)
        data = r.json()
        os.makedirs(path)
        md5list = open(f"{path}/list", "w")
        for p in data:
            md5hash = p['md5']
            md5list.write(f"{md5hash}\n")
        md5list.close()

    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return

    return data

def download_samples():
    hashlist = download_hashlist()
#    md5list = open(f"{path}/list", "w")

    for p in hashlist:
        md5hash = p['md5']
        getfile = {'action': 'getfile', 'api_key': api_key, 'hash': md5hash}
        r = requests.get(url, params = getfile)
        sample = r.content

        with open(os.path.join(path, md5hash), mode = "wb") as fh:
            fh.write(sample)

#        md5list.write(f"{md5hash}\n")

#    md5list.close()

if __name__ == "__main__":
    download_samples()
