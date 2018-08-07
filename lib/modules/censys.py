#!/usr/bin/env python
##
# omnibus - deadbits.
# censys.io module
##

from http import get

from common import get_apikey
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['censys'] = None
        self.api_key = get_apikey('censys')
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def run(self):
        url = 'https://censys.io/api/v1/view/ipv4/%s' % self.artifact['name']

        try:
            status, response = get(url, auth=(self.api_key['token'], self.api_key['secret']), headers=self.headers)

            if status:
                self.artifact['data']['censys'] = response.json()
        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
