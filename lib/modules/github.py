#!/usr/bin/env python
##
# omnibus - deadbits
# search github for active users
##
from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['github'] = None


    def run(self):
        url = 'https://api.github.com/users/%s' % self.artifact['name']
        headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

        try:
            status, response = get(url, headers=headers)
            if status:
                self.artifact.data['github'] = response.json()

                if 'email' in self.artifact.data['github'].keys():
                    if self.artifact.data['github']['email']:
                        self.artifact['children'].append({
                            'name': self.artifact.data['github']['email'],
                            'type': 'email',
                            'subtype': None,
                            'source': 'github'
                        })
        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
