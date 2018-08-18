#!/usr/bin/env python
##
# omnibus - deadbits
# hurricane eletric
##
import re

from BeautifulSoup import BeautifulSoup

from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['he'] = None


    def ip(self):
        url = 'http://bgp.he.net/ip/%s#_dns' % self.artifact['name']
        headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

        try:
            status, response = get(url, headers=headers)

            if status:
                result = []
                data = BeautifulSoup(response.text)

                for item in data.findAll(attrs={'id': 'dns', 'class': 'tabdata hidden'}):
                    result.append(item.text.strip())

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


    def fqdn(self):
        url = 'http://bgp.he.net/dns/%s#_whois' % self.artifact['name']
        headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

        try:
            status, response = get(url, headers=headers)

            result = []
            if status:
                pattern = re.compile('\/dns\/.+\".title\=\".+\"\>(.+)<\/a\>', re.IGNORECASE)
                hosts = re.findall(pattern, response.text)
                for h in hosts:
                    result.append(h.strip())
        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


    def run(self):
        if self.artifact['subtype'] == 'ipv4':
            self.artifact['data']['he'] = self.ip()

        elif self.artifact['subtype'] == 'fqdn':
            self.artifact['data']['he'] = self.fqdn()


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
