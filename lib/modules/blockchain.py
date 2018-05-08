#!/usr/bin/env python
##
# omnibus - deadbits
# blockchain.info address lookup
##
from http import get


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['blockchain'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    def run(self):
        url = 'https://blockchain.info/rawaddr/%s' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)
            if status:
                self.artifact['data']['blockchain'] = response.json()
        except:
            pass


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
