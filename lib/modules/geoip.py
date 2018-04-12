#!/usr/bin/env python
##
# omnibus - deadbits.
# geolocation for hosts
##
from common import error
from common import http_get


def run(host):
    results = None
    url = 'http://freegeoip.net/json/%s' % host
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'
    }

    try:
        status, response = http_get(url, headers=headers)
    except:
        error('failed to get GeoIP results (%s)' % host)
        return results

    if status:
        results = response.json()

    return results
