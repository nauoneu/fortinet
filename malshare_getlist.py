#! /usr/bin/env python
# Download files with given hashes.json file

import requests
import argparse
import json
import logging
import os
import sys
from pprint import pprint

#with open('list.json') as json_file:
#    data = json.load(json_file)

# global vars
api_key = "14b204a8ff4fdc3e6f0a7a0aee38446eb2d560c10d76bae2e8980043d5d628af"
url = "https://malshare.com/api.php"
getlist = {'action': 'getlist', 'api_key': api_key}


def download_hashlist():
    try:
#        r = requests.get(url, params = getlist)
#        print(api_key)
#        print(r.url)
#        pprint(r.json())
#        pprint(data)
#        for p in data:
#            print('MD5: ' + p['md5'])
        with open('list.json') as json_file:
            data = json.load(json_file)

#    except requests.exceptions.RequestException as e:
#        print(e, file=sys.stderr)
#        return

    except Exception as e:
        print(e)
        return

    return data

def download_samples():
    hashlist = download_hashlist()
    count = 0
    for p in hashlist:
#        if count < 1:
#            md5hash = p['md5']
#            getfile = {'action': 'getfile', 'api_key': api_key, 'hash': md5hash}
#            r = requests.get(url, params = getfile)
#            sample = r.content
#
#            with open(os.path.join("files", md5hash), mode = "wb") as fh:
#                fh.write(sample)
#
#            count += 1
#
#        else:
#            return
        count += 1
    print(count)

if __name__ == "__main__":
    download_samples()
