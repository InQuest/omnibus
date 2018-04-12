#!/usr/bin/env python
##
# omnibus - deadbits.
# query SANS ISC API
##
from common import is_ipv4
from common import http_get


def run(host):
    if is_ipv4(host):
        result = None
        url = 'https://isc.sans.edu/api/ip/%s?json' % host
        headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

        try:
            status, response = http_get(url, headers=headers)
        except:
            return result

        if status:
            data = response.json()
            result = {
                'count': data['count']['text'],
                'attacks': data['attacks']['text'],
                'mindate': data['mindate']['text'],
                'maxdate': data['maxdate']['text']
            }

        return result
