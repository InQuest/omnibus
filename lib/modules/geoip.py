#!/usr/bin/env python
##
# omnibus - deadbits.
# geolocation for hosts
##
from http import get

from common import get_apikey
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['geoip'] = None
        self.api_key = get_apikey('ipstack')
        if self.api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def run(self):
        url = 'http://api.ipstack.com/%s?access_key=%s&hostname=1' % (self.artifact['name'], self.api_key)

        try:
            status, response = get(url, headers=self.headers)

            if status:
                results = response.json()
                self.artifact['data']['geoip'] = results


                if 'hostname' in results.keys():
                    if results['hostname'] != self.artifact['name'] and results['hostname'] != '':
                        self.artifact.children.append({
                            'name': results['hostname'],
                            'type': 'host',
                            'subtype': 'fqdn',
                            'source': 'ipstack'
                        })
        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
