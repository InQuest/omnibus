#!/usr/bin/env python
##
# omnibus - deadbits.
# keybase user search
##
from common import http_get


def run(user):
    url = 'https://keybase.io/_/api/1.0/user/lookup.json?usernames=%s' % user

    resp = http_get(url)
    if resp[0]:
        jdata = resp[1].json()

        if jdata['them'][0] is not None:
            return jdata['them'][0]
        else:
            return None
