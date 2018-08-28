#!/usr/bin/env python
##
# omnibus - deadbits.
# ipinfo module
##
from http import get

from common import warning
from common import get_apikey


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['ipinfo'] = None
        self.api_key = get_apikey('ipinfo')
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def run(self):
        if self.api_key == '':
            error('API keys cannot be left blank | set all keys in etc/apikeys.json')
            return

        url = 'http://ipinfo.io/{}/json?token={}'.format(self.artifact['name'], self.api_key)

        try:
            status, response = get(url, headers=self.headers)

            if status:
                self.artifact['data']['ipinfo'] = response.json()

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
