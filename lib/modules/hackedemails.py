#!/usr/bin/env python
##
# omnibus - deadbits
# hacked-emails.com
##
from common import error
from common import http_get


def run(email_addr):
    results = None
    url = 'https://hacked-emails.com/api?q=%s' % email_addr
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        error('failed to get Hacked-Emails.com results (%s)' % email_addr)
        return results

    if status:
        results = response.json()

    return results
