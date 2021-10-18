#! /usr/bin/env python
# Download files with given hashes.json file

import requests
import argparse
import json
import logging
import os
import shutil
import datetime
import sys
from pprint import pprint

# global vars
api_key = "your_key"
url = "https://malshare.com/api.php"
getlist = {'action': 'getlist', 'api_key': api_key}
now = datetime.datetime.now()
pdate = now - datetime.timedelta(days=14)
folder = now.strftime('%Y-%m-%d-%H')
pfolder = pdate.strftime('%Y-%m-%d-%H')
#folder = f"{now.year}-{now.month}-{now.day}-{now.hour}"
path = f"/var/www/html/files/{folder}"
ppath = f"/var/www/html/files/{pfolder}"

def download_hashlist():
    try:
        r = requests.get(url, params = getlist)
        data = r.json()
        shutil.rmtree(ppath, ignore_errors=True)
        os.makedirs(path)
        md5list = open(f"{path}/list", "w")
        for p in data:
            md5hash = p['md5']
            md5list.write(f"{md5hash}\n")
        md5list.close()

    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return

    except OSError as e:
        print(e, file=sys.stderr)
        pass

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
#    download_samples()
    download_hashlist()
