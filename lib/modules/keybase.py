#!/usr/bin/env python
##
# omnibus - deadbits.
# keybase user search
##
from common import http_get


def run(user):
    result = None
    url = 'https://keybase.io/_/api/1.0/user/lookup.json?usernames=%s' % user

    try:
        status, response = http_get(url)
    except:
        return result

    if status:
        data = response.json()
        if data['them'][0] is not None:
            result = data['them'][0]

    return result
