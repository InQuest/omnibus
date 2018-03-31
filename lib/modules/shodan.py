#!/usr/bin/env python
##
# omnibus - deadbits.
# shodan search
##
import requests

from lib.common import get_apikey


def domain(host):
    result = {}

    api_key = get_apikey('shodan')
    url = 'https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}' % (api_key, host)

    try:
        resp = requests.get(url)
    except:
        return result

    return resp.json()


def ip(host):
    result = {}

    api_key = get_apikey('shodan')
    url = 'https://api.shodan.io/shodan/host/%s?key=%s' % (host, api_key)

    try:
        resp = requests.get(url)
    except:
        return result

    return resp.json()
