#!/usr/bin/env python
##
# omnibus - deadbits.
# resolve dns records
##

import dns.resolver

from common import warning
from common import detect_type


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['dnsresolve'] = None


    def get_record(self, domain, record):
        results = []

        try:
            res = dns.resolver.query(domain, record)
            for item in res:
                if item.endswith('.'):
                    item = item.rstrip('.')
                if item not in results:
                    results.append(str(item))
        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))
            results.append(None)

        return results


    def run(self):
        domain = self.artifact['name']

        self.artifact['data']['dnsresolve'] = {
            'A': 'Not Found',
            'AAAA': 'Not Found',
            'CNAME': 'Not Found',
            'NS': 'Not Found',
            'MX': 'Not Found',
            'TXT': 'Not Found'
        }

        for key in self.artifact['data']['dnsresolve'].keys():
            self.artifact['data']['dnsresolve'][key] = self.get_record(domain, key)

        # self.artifact['data']['dnsresolve']['A'] = self.get_record(domain, 'A')
        # self.artifact['data']['dnsresolve']['AAAA'] = self.get_record(domain, 'AAAA')
        # self.artifact['data']['dnsresolve']['CNAME'] = self.get_record(domain, 'CNAME')
        # self.artifact['data']['dnsresolve']['NS'] = self.get_record(domain, 'NS')
        # self.artifact['data']['dnsresolve']['MX'] = self.get_record(domain, 'MX')
        # self.artifact['data']['dnsresolve']['TXT'] = self.get_record(domain, 'TXT')

        for host in self.artifact['data']['dnsresolve']:
            if isinstance(host, str):
                if detect_type(host) == 'host':
                    entry = {
                        'name': host,
                        'type': 'host',
                        'source': 'DNS resolution',
                        'subtype': None
                    }
                    self.artifact['children'].append(entry)

            elif isinstance(host, list):
                for h in host:
                    if detect_type(h) == 'host':
                        entry = {
                            'name': h,
                            'type': 'host',
                            'source': 'DNS resolution',
                            'subtype': None
                        }
                        self.artifact['children'].append(entry)


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
