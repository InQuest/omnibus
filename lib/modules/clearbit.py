#!/usr/bin/env python
##
# omnibus - deadbits.
# clearbit email lookup module
##
from http import get

from common import warning
from common import get_apikey


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['clearbit'] = None

        self.api_key = get_apikey('clearbit')
        if self.api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')

        self.headers = {
            'Authorization': 'Bearer %s' % self.api_key,
            'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'
        }

    def run(self):
        url = 'https://person.clearbit.com/v1/people/email/%s' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)

            if status:
                if 'error' in response.content and 'queued' in response.content:
                    warning('results are queued by Clearbit. please re-run module after 5-10 minutes.')
                else:
                    self.artifact['data']['fullcontact'] = response.json()

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
