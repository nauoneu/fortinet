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
import time
from pprint import pprint

# global vars
homedir = "/home/tueno/files"
now = datetime.datetime.now()
pdate = now - datetime.timedelta(days=14)
folder = now.strftime('%Y-%m-%d-%H')
pfolder = pdate.strftime('%Y-%m-%d-%H')
#folder = f"{now.year}-{now.month}-{now.day}-{now.hour}"
path = f"{homedir}/{folder}"
ppath = f"{homedir}/{pfolder}"
url = f"http://10.130.8.158/files/{folder}"

def download_hashlist():
    try:
#        print(url)
        r = requests.get(f"{url}/list")
#        print(r.text)
        shutil.rmtree(ppath, ignore_errors=True)
        os.makedirs(path)

    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return

    return r.text

def download_samples():
    hashlist = download_hashlist().split("\n")

    for p in hashlist:
#        print(p)
#        rpath = f"http://10.130.8.158/files/{folder}/{p}"
        rpath = f"{url}/{p}"
        r = requests.get(rpath)
        sample = r.content

        with open(os.path.join(path, p), mode = "wb") as fh:
            fh.write(sample)

        time.sleep(1)

if __name__ == "__main__":
    download_samples()
