#!/usr/bin/env python
##
# omnibus - deadbits.
# virustotal module
##
from http import get

from common import get_apikey
from common import detect_type


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['virustotal'] = None
        self.api_key = get_apikey('virustotal')
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'
        }


    def ip(self):
        parameters = {'ip': self.artifact['name'], 'apikey': self.api_key}
        url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'

        try:
            status, response = get(url, params=parameters)

            if status:
                data = response.json()
                if data['response_code'] == 1:
                    self.artifact['data']['virustotal'] = data

                    if len(data['resolutions']) > 0:
                        for host in data['resolutions']:
                            if detect_type(host['hostname']) == 'host':
                                self.artifact['children'].append({
                                    'name': host['hostname'],
                                    'type': 'host',
                                    'subtype': 'fqdn',
                                    'source': 'VirusTotal'
                                })

        except:
            pass


    def fqdn(self):
        parameters = {'domain': self.artifact['name'], 'apikey': self.api_key}
        url = 'https://www.virustotal.com/vtapi/v2/domain/report'

        try:
            status, response = get(url, params=parameters)

            if status:
                data = response.json()
                if data['response_code'] == 1:
                    self.artifact['data']['virustotal'] = data

                    if len(data['resolutions']) > 0:
                        for host in data['resolutions']:
                            if detect_type(host['ip_address']) == 'host':
                                self.artifact['children'].append({
                                    'name': host['ip_address'],
                                    'type': 'host',
                                    'subtype': 'ipv4',
                                    'source': 'VirusTotal'
                                })
        except:
            pass


    def hash(self):
        parameters = {'resource': self.artifact['name'], 'apikey': self.api_key}
        url = 'https://www.virustotal.com/vtapi/v2/file/report'


        try:
            status, response = get(url, params=parameters)

            if status:
                data = response.json()

                if data['response_code'] == 1:
                    for av in data['scans'].keys():
                        if data['scans'][av]['detected'] is False:
                            del data['scans'][av]

                    self.artifact['data']['virustotal'] = data
        except:
            pass


    def run(self):
        if self.artifact['type'] == 'host':
            if self.artifact['subtype'] == 'ipv4':
                self.ip()
            elif self.artifact['subtype'] == 'fqdn':
                self.fqdn()
        elif self.artifact['type'] == 'hash':
            self.hash()


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
