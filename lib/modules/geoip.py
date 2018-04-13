#!/usr/bin/env python
##
# omnibus - deadbits.
# geolocation for hosts
##
from http import get

from common import error


def run(host):
    results = None
    url = 'http://freegeoip.net/json/%s' % host
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'
    }

    try:
        status, response = get(url, headers=headers)
    except:
        error('failed to get GeoIP results (%s)' % host)
        return results

    if status:
        results = response.json()
        del results['__deprecation_message__']

    return results


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
