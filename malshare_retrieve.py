#! /usr/bin/env python
# Download files with given hashes.json file

import requests
import argparse
import json
import logging
import os
import datetime
import sys
import time
from pprint import pprint

# global vars
#api_key = "14b204a8ff4fdc3e6f0a7a0aee38446eb2d560c10d76bae2e8980043d5d628af"
today = datetime.date.today()
url = f"http://10.130.8.158/files/{today}"
#getlist = {'action': 'getlist', 'api_key': api_key}
path = f"files/{today}"

def download_hashlist():
    try:
#        print(url)
        r = requests.get(f"{url}/list")
#        print(r.text)
        os.makedirs(path)

    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return

    return r.text

def download_samples():
    hashlist = download_hashlist().split("\n")

    for p in hashlist:
#        print(p)
        rpath = f"http://10.130.8.158/files/{today}/{p}"
        r = requests.get(rpath)
        sample = r.content

        with open(os.path.join(path, p), mode = "wb") as fh:
            fh.write(sample)

        time.sleep(1)

if __name__ == "__main__":
    download_samples()
