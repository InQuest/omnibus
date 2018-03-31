#!/usr/bin/env python
##
# omnibus - deadbits.
# ipvoid module
##
import requests
import BeautifulSoup

from common import is_ipv4


def ipvoid_check(ip):
    result = {}
    if not is_ipv4(ip):
        return None

    headers = {'User-Agent': 'OSINT Omnibus (github.com/deadbits/omnibus)'}
    url = 'http://ipvoid.com/scan/%s/' % ip
    try:
        response = requests.get(url, headers=headers)
    except:
        return result

    data = BeautifulSoup(response.text)

    if data.findAll('span', attrs={'class': 'label label-success'}):
        return None

    elif data.findAll('span', attrs={'class': 'label label-danger'}):
        for each in data.findAll('img', alt='Alert'):
            site = each.parent.parent.td.text.lstrip()
            url = each.parent.a['href']
            result[site] = url

    return result
