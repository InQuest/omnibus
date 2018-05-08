#!/usr/bin/env python
##
# omnibus - deadbits.
# threatcrowd module
##
import threatcrowd

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['threatcrowd'] = None


    def ip(self):
        try:
            self.artifact['data']['threatcrowd'] = threatcrowd.ip_report(self.artifact['name'])
        except:
            pass


    def fqdn(self):
        try:
            self.artifact['data']['threatcrowd'] = threatcrowd.domain_report(self.artifact['name'])
        except:
            pass


    def run(self):
        if self.artifact['subtype'] == 'ipv4':
            self.ip()
        elif self.artifact['subtype'] == 'fqdn':
            self.fqdn()
        else:
            warning('Threatcrowd module only supports artifacts of type ipv4 or fqdn')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
