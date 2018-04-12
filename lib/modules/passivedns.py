#!/usr/bin/env python
##
# omnibus - deadbits.
# passivetotal.com module
##
from requests.auth import HTTPBasicAuth

from common import get_apikey
from common import http_get


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
