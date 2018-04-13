#!/usr/bin/env python
##
# omnibus - deadbits.
# shodan search
##
from http import get

from common import get_apikey


def fqdn_run(host):
    result = None
    api_key = get_apikey('shodan')
    url = 'https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}' % (api_key, host)
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

    try:
        status, response = get(url, headers=headers)
    except:
        return result

    if status:
        result = response.json()

    return result


def ip_run(host):
    result = None
    api_key = get_apikey('shodan')
    url = 'https://api.shodan.io/shodan/host/%s?key=%s' % (host, api_key)
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

    try:
        status, response = get(url, headers=headers)
    except:
        return result

    if status:
        result = response.json()

    return result


def main(artifact, artifact_type):
    if artifact_type == 'ipv4':
        result = ip_run(artifact)
    elif artifact_type == 'fqdn':
        result = fqdn_run(artifact)
    else:
        return None

    return result
