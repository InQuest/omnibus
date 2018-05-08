#!/usr/bin/env python
##
# omnibus - deadbits
# haveibeenpwned
##
from http import get


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['hibp'] = {'breaches': None, 'pastes': None}
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def breaches(self):
        url = 'https://haveibeenpwned.com/api/v2/breachedaccount/%s' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)
            if status:
                self.artifact['data']['hibp']['breaches'] = response.json()
        except:
            pass


    def pastes(self):
        url = 'https://haveibeenpwned.com/api/v2/pasteaccount/%s' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)
            if status:
                self.artifact['data']['hibp']['pastes'] = response.json()
        except:
            pass


    def run(self):
        self.artifact['data']['hibp'] = {'breaches': None, 'pastes': None}
        self.breaches()
        self.pastes()



def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
