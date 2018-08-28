#!/usr/bin/env python
##
# omnibus - deadbits.
# ipvoid module
##
from BeautifulSoup import BeautifulSoup

from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['ipvoid'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def run(self):
        url = 'http://www.ipvoid.com/scan/%s/' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)

            if status:
                data = BeautifulSoup(response.text)

                if data.findAll('span', attrs={'class': 'label label-success'}):
                    pass

                elif data.findAll('span', attrs={'class': 'label label-danger'}):
                    for each in data.findAll('img', alt='Alert'):
                        site = each.parent.parent.td.text.lstrip()
                        url = each.parent.a['href']
                        self.artifact['data']['ipvoid'] = {site: url}

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    if artifact['subtype'] == 'ipv4':
        plugin = Plugin(artifact)
        plugin.run()
    else:
        warning('IPVoid only accepts artifacts of subtype IPv4')

    return plugin.artifact
