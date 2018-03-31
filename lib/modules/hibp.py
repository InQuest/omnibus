#!/usr/bin/env python
##
# omnibus - deadbits
# haveibeenpwned
##
import requests

from lib.common import warning


def run(email_addr):
    url = 'https://haveibeenpwned.com/api/v1/breachedaccount/%s' % email_addr

    try:
        resp = requests.get(url)
        if 'Attention Required! | CloudFlare' in resp.content:
            warning('CloudFlare detected; please try module again later.')
        return resp.jdata()
    except:
        return None
