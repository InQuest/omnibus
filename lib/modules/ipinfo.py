#!/usr/bin/env python
##
# omnibus - deadbits.
# ipinfo module
##
from http import get


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['ipinfo'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def run(self):
        url = 'http://ipinfo.io/%s/json' % self.artifact['name']

        try:
            status, response = get(url, auth=(self.api_key['token'], self.api_key['secret']), headers=self.headers)

            if status:
                self.artifact['data']['ipinfo'] = response.json()
        except:
            pass


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
