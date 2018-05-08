#!/usr/bin/env python
##
# omnibus - deadbits.
# resolve dns records
##

import dns.resolver

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
                if item not in results:
                    results.append(str(item))
        except:
            results.append(None)

        return results


    def run(self):
        domain = self.artifact['name']

        self.artifact['data']['dnsresolve'] = {
            'A': None,
            'AAAA': None,
            'CNAME': None,
            'NS': None,
            'MX': None,
            'TXT': None
        }

        self.artifact['data']['dnsresolve']['A'] = self.get_record(domain, 'A')
        self.artifact['data']['dnsresolve']['AAAA'] = self.get_record(domain, 'AAAA')
        self.artifact['data']['dnsresolve']['CNAME'] = self.get_record(domain, 'CNAME')
        self.artifact['data']['dnsresolve']['NS'] = self.get_record(domain, 'NS')
        self.artifact['data']['dnsresolve']['MX'] = self.get_record(domain, 'MX')
        self.artifact['data']['dnsresolve']['TXT'] = self.get_record(domain, 'TXT')

        for item in self.artifact['data']['dnsresolve']:
            if isinstance(item, str):
                if detect_type(item) == 'host':
                    entry = {
                        'name': item,
                        'type': 'host',
                        'source': 'DNS resolution',
                        'subtype': None
                    }
                    self.artifact['children'].append(entry)
            elif isinstance(item, list):
                for i in item:
                    if detect_type(i) == 'host':
                        entry = {
                            'name': i,
                            'type': 'host',
                            'source': 'DNS resolution',
                            'subtype': None
                        }
                        self.artifact['children'].append(entry)


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
