#!/usr/bin/env python
##
# omnibus - deadbits.
# keybase user search
##

from ..common import warning
from ..http import get


class Plugin(object):

    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['keybase'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    def run(self):
        url = 'https://keybase.io/_/api/1.0/user/lookup.json?usernames=%s' % self.artifact['name']

        try:
            status, response = get(url, auth=(self.api_key['token'], self.api_key['secret']), headers=self.headers)

            if status:
                data = response.json()
                if data['them'][0] is not None:
                    self.artifact['data']['keybase'] = data['them'][0]
        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
