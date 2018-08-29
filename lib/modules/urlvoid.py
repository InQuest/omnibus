#!/usr/bin/env python
##
# omnibus - deadbits.
# urlvoid module - from yolothreat's utilitybelt
##
from BeautifulSoup import BeautifulSoup

from http import get
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['urlvoid'] = None
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'
        }


    def run(self):
        url = 'http://urlvoid.com/scan/%s/' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)

            if status:
                data = BeautifulSoup(response.text)

                if data.findAll('div', attrs={'class': 'bs-callout bs-callout-info'}):
                    pass

                elif data.findAll('div', attrs={'class': 'bs-callout bs-callout-warning'}):
                    self.artifact['data']['urlvoid'] = {}
                    for each in data.findAll('img', alt='Alert'):
                        site = each.parent.parent.td.text.lstrip()
                        url = each.parent.a['href']
                        self.artifact['data']['urlvoid'][site] = url

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
