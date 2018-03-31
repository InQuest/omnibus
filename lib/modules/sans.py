#!/usr/bin/env python
##
# omnibus - deadbits.
# query SANS ISC API
##

import requests

from common import is_ipv4


def run(host):
    if is_ipv4(host):
        url = 'https://isc.sans.edu/api/ip/%s?json' % host
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36'}

        try:
            response = requests.get(url, headers=headers)
        except:
            return None

        data = response.json()

        return {'count': data['count']['text'],
                'attacks': data['attacks']['text'],
                'mindate': data['mindate']['text'],
                'maxdate': data['maxdate']['text']}
    else:
        return None
