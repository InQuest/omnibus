#!/usr/bin/env python
##
# omnibus - deadbits
# nmap scanner
##
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser

from ..common import warning


class Plugin(object):

    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['nmap'] = None

    def run(self):
        nm = NmapProcess(targets=str(self.artifact['name']), options='-sT -sV -Pn -T5 -p21,22,23,25,80,6667,1337')
        nm.run()

        if nm.is_successful():
            report = NmapParser.parse_fromstring(nm.stdout)
            for host in report.hosts:
                if host.is_up():
                    results = {
                        'ports': host.get_open_ports(),
                        'services': []
                    }

                    for service in host.services:
                        if service.state == 'open':
                            serv = {
                                'banner': service.banner,
                                'protocol': service.protocol,
                                'service': service.service,
                                'port': service.port}
                            results['services'].append(serv)

                    if self.artifact['subtype'] == 'ipv4':
                        results['hostnames'] = host.hostnames
                        for h in host.hostnames:
                            self.artifact['children'].append({
                                'name': h,
                                'type': 'host',
                                'subtype': 'fqdn',
                                'source': 'Nmap'
                            })

                    elif self.artifact['subtype'] == 'fqdn':
                        results['ipv4'] = host.address
                        self.artifact['children'].append({
                            'name': host.address,
                            'type': 'host',
                            'subtype': 'ipv4',
                            'source': 'Nmap'
                        })

                    self.artifact['data']['nmap'] = results

        else:
            warning('Nmap scanner failed - no results')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
