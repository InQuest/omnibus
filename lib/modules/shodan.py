#!/usr/bin/env python
##
# omnibus - deadbits.
# shodan search
##

from common import http_get
from common import get_apikey


def domain(host):
    result = None
    api_key = get_apikey('shodan')
    url = 'https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}' % (api_key, host)
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        return result

    if status:
        result = response.json()

    return result


def ip(host):
    result = None
    api_key = get_apikey('shodan')
    url = 'https://api.shodan.io/shodan/host/%s?key=%s' % (host, api_key)
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        return result

    if status:
        result = response.json()

    return result
