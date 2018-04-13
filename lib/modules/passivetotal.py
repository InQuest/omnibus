#!/usr/bin/env python
##
# omnibus - deadbits.
# passivetotal.com module
##
from requests.auth import HTTPBasicAuth

from http import http_get

from common import get_apikey


def run(host):
    result = None
    key = get_apikey('passivetotal')
    url = 'https://api.passivetotal.org/v2/dns/passive/unique?query=%s' % host

    user = key['user']
    token = key['key']

    try:
        status, response = http_get(url, auth=HTTPBasicAuth(user, token))
    except:
        return result

    if status:
        data = response.json()
        result = data['results']

    return result


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
