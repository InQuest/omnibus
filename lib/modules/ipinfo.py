#!/usr/bin/env python
##
# omnibus - deadbits.
# ipinfo module
##
from http import get


def run(host):
    results = None
    url = 'http://ipinfo.io/%s/json' % host
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

    try:
        status, response = get(url, headers=headers)
    except:
        return results

    if status:
        results = response.json()

    return results


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
