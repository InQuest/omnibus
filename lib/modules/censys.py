#!/usr/bin/env python
##
# omnibus - deadbits.
# censys.io module
##
from http import http_get

from common import get_apikey


def run(host):
    result = None
    key = get_apikey('censys')
    url = 'https://censys.io/api/v1/view/ipv4/%s' % host
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    try:
        status, response = http_get(url, auth=(key['token'], key['secret']), headers=headers)
    except:
        return result

    if status:
        result = response.json()

    return result


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
