#!/usr/bin/env python
##
# omnibus - deadbits.
# shodan search
##
from http import get

from common import get_apikey


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['shodan'] = None
        self.api_key = get_apikey('shodan')
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus'}

    def fqdn(self):
        url = 'https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}' % (self.api_key, self.artifact['name'])

        try:
            status, response = get(url, headers=self.headers)

            if status:
                self.artifact['data']['shodan'] = response.json()
        except:
            pass


    def ip(self):
        url = 'https://api.shodan.io/shodan/host/%s?key=%s' % (self.artifact['name'], self.api_key)

        try:
            status, response = get(url, headers=self.headers)

            if status:
                self.artifact['data']['shodan'] = response.json()
        except:
            pass


    def run(self):
        if self.artifact['subtype'] == 'ipv4':
            self.ip()
        elif self.artifact['subtype'] == 'fqdn':
            self.fqdn()


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
