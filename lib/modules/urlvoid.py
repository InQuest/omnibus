#!/usr/bin/env python
##
# omnibus - deadbits.
# urlvoid module - from yolothreat's utilitybelt
##
import requests

from bs4 import BeautifulSoup


def run(host):
    result = {}

    try:
        resp = requests.get('http://urlvoid.com/scan/%s/' % host)
    except:
        return result

    data = BeautifulSoup(resp.text)

    if data.findAll('div', attrs={'class': 'bs-callout bs-callout-info'}):
        return None

    elif data.findAll('div', attrs={'class': 'bs-callout bs-callout-warning'}):
        for each in data.findAll('img', alt='Alert'):
            site = each.parent.parent.td.text.lstrip()
            url = each.parent.a['href']
            result[site] = url
    else:
        return None

    if len(result) == 0:
        return None

    return result
