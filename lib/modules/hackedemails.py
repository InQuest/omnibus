#!/usr/bin/env python
##
# omnibus - deadbits
# hacked-emails.com
##
import requests


def run(email_addr):
    url = 'https://hacked-emails.com/api?q=%s' % email_addr

    try:
        resp = requests.get(url)
        return resp.jdata()
    except:
        return None
