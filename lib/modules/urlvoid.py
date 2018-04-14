#!/usr/bin/env python
##
# omnibus - deadbits.
# urlvoid module - from yolothreat's utilitybelt
##
from BeautifulSoup import BeautifulSoup

from http import get


def run(host):
    result = {}

    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}
    url = 'http://urlvoid.com/scan/%s/' % host
    try:
        status, response = get(url, headers=headers)
    except:
        return result

    if status:
        data = BeautifulSoup(response.text)

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


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
