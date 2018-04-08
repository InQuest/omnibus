#!/usr/bin/env python
##
# omnibus - deadbits
# search github for active users
##
from common import error
from common import http_get


def run(username):
    results = None
    url = 'https://api.github.com/users/%s' % username
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/deadbits/omnibus)'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        error('failed to get Github results (%s)' % username)
        return results

    if status:
        results = response.json()

    return results
