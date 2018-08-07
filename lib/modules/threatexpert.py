#!/usr/bin/env python
##
# omnibus - deadbits.
# threatexpert module
##
from BeautifulSoup import BeautifulSoup

from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['threatexpert'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    def run(self):
        url = 'http://www.threatexpert.com/reports.aspx?find=%s' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)

            if status:
                if 'no ThreatExpert reports found' in response.text:
                    pass

                self.artifact['data']['threatexpert'] = []
                content = BeautifulSoup(response.text, 'html.parser')
                rows = content.find('span', id='txtResults').find_all('tr')

                for row in rows:
                    items = row.find_all('td')[3].text
                    if '(not available)' not in items and 'Findings' not in items:
                        self.artifact['data']['threatexpert'].append(items.strip())
        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
