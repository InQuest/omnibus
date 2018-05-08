#!/usr/bin/env python
##
# omnibus - deadbits.
# cymon.io module
##
import cymon

from common import get_apikey


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['cymon'] = None
        self.api_key = get_apikey('cymon')
        self.api = cymon.Cymon(self.api_key)



    def ip(self):
        try:
            self.artifact['data']['cymon'] = self.api.ip_lookup(self.artifact['name'])
        except:
            pass


    def fqdn(self):
        try:
            self.artifact['data']['cymon'] = self.api.domain_lookup(self.artifact['name'])
        except:
            pass


    def run(self):
        if self.artifact['subtype'] == 'ipv4':
            self.ip()
        elif self.artifact['subtype'] == 'fqdn':
            self.fqdn()


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
