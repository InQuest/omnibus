#!/usr/bin/env python
##
# omnibus - deadbits.
# whois module
##
import whois

from ipwhois import IPWhois


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['whois'] = None


    def ip(self):
        whois = IPWhois(self.artifact['name'])

        try:
            data = whois.lookup_rdap(depth=1)

            if data is not None:
                self.artifact['data']['whois'] = {}
                self.artifact['data']['whois']['ASN'] = data['asn']
                self.artifact['data']['whois']['Organization'] = data['network']['name'] if 'network' in data.keys() else None
                self.artifact['data']['whois']['CIDR'] = data['network']['cidr'] if 'network' in data.keys() else None
                self.artifact['data']['whois']['Country'] = data['network']['cidr'] if 'network' in data.keys() else None
        except:
            pass


    def fqdn(self):
        try:
            results = whois.whois(self.artifact['name'])
            self.artifact['data']['whois'] = results
        except:
            pass


    def run(self):
        if self.artifact['type'] == 'host':
            if self.artifact['subtype'] == 'ipv4':
                self.ip()
            elif self.artifact['subtype'] == 'fqdn':
                self.fqdn()


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
