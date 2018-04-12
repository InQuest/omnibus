#!/usr/bin/env python
##
# omnibus - deadbits.
# ipinfo module
##
from common import error
from common import http_get


def run(host):
    results = None
    url = 'http://ipinfo.io/%s/json' % host
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        error('failed to get IPVoid results (%s)' % host)
        return results

    if status:
        results = response.json()

    return results
