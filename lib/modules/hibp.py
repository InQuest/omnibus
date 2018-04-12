#!/usr/bin/env python
##
# omnibus - deadbits
# haveibeenpwned
##

from common import warning
from common import http_get


def run(email_addr):
    results = None
    url = 'https://haveibeenpwned.com/api/v1/breachedaccount/%s' % email_addr
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        return results

    if status:
        if 'Attention Required! | CloudFlare' in response.content:
            warning('CloudFlare detected; please try module again later.')
        else:
            results = response.json()

    return results
