#!/usr/bin/env python
##
# omnibus - deadbits.
# whois module
##

import whois
from ipwhois import IPWhois

from ..common import warning


class Plugin(object):

    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['whois'] = None

    def ip(self):
        whois_data = IPWhois(self.artifact['name'])

        try:
            data = whois_data.lookup_whois()

            if data is not None:
                self.artifact['data']['whois'] = {}

                # collect ASN information

                self.artifact['data']['whois']['asn'] = data['asn']
                self.artifact['data']['whois']['asn']['cidr'] = data['asn_cidr']
                self.artifact['data']['whois']['asn']['description'] = data['asn_description']
                self.artifact['data']['whois']['asn']['country'] = data['asn_country_code']

                if 'nets' in data.keys() and len(data['nets']) > 0:
                    net_data = data['nets'][0]
                    self.artifact['data']['whois']['address'] = net_data['address']
                    self.artifact['data']['whois']['state'] = net_data['state']
                    self.artifact['data']['whois']['emails'] = net_data['emails']

        except Exception as err:
            warning('Caught unhandled exception: %s' % str(err))

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
