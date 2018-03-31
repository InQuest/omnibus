#!/usr/bin/env python
##
# omnibus - deadbits.
# geolocation for hosts
##
import requests


def run(host):
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'OSINT Omnibus (https://github.com/deadbits/omnibus)'
    }

    try:
        resp = requests.get('http://freegeoip.net/json/%s' % host, headers=headers)
        jdata = resp.json()
        return jdata
    except Exception:
        return None
