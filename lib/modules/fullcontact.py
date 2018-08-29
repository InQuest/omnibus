#!/usr/bin/env python
##
# omnibus - deadbits
# fullcontact.com
##
from http import get

from common import get_apikey
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['fullcontact'] = None
        self.api_key = get_apikey('fullcontact')
        if self.api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')
        self.headers = {
            'X-FullContact-APIKey': self.api_key,
            'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'
        }


    def run(self):
        try:
            status, response = get('https://api.fullcontact.com/v2/person.json?email=%s' % self.artifact['name'],
                headers=self.headers)

            if status:
                self.artifact['data']['fullcontact'] = response.json()

                if 'socialProfiles' in self.artifact['data']['fullcontact'].keys():
                    for profile in self.artifact['data']['fullcontact']['socialProfiles']:
                        child = {
                            'type': 'user',
                            'name': profile['username'],
                            'source': 'fullcontact',
                            'subtype': profile['type']
                        }
                        self.artifact['children'].append(child)

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
