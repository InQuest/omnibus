#!/usr/bin/env python
##
# omnibus - deadbits.
# threatminer module
##

from ..common import detect_type
from ..common import warning
from ..http import get


class Plugin(object):

    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['threatminer'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    def ip(self):
        url = 'https://api.threatminer.org/v2/host.php?q=%s&rt=2' % self.artifact['name']

        # check for passive DNS results
        try:
            status, response = get(url)
            if status:
                data = response.json()

                if data['status_code'] == '200' and 'status_message' == 'Results found.':
                    self.artifact['data']['threatminer'] = {'passivedns': data['results']}

                # check for potential children artifacts
                if isinstance(self.artifact['data']['threatminer'], dict):
                    for entry in self.artifact['data']['threatminer']['passivedns']:
                        if detect_type(entry['domain']) == 'host':
                            self.artifact['children'].append({
                                'name': entry['domain'],
                                'type': 'host',
                                'subtype': 'fqdn',
                                'source': 'threatminer'
                            })

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))

    def fqdn(self):
        sub_url = 'https://api.threatminer.org/v2/domain.php?q=%s&rt=5' % self.artifact['name']
        pdns_url = 'https://api.threatminer.org/v2/domain.php?q=%s&rt=2' % self.artifact['name']

        # check for passive DNS results
        try:
            status, response = get(pdns_url)
            if status:
                data = response.json()

                if data['status_code'] == '200' and 'status_message' == 'Results found.':
                    self.artifact['data']['threatminer'] = {'passivedns': data['results']}

                # check for potential children artifacts
                if isinstance(self.artifact['data']['threatminer'], dict):
                    for entry in self.artifact['data']['threatminer']['passivedns']:
                        if detect_type(entry['domain']) == 'host':
                            self.artifact['children'].append({
                                'name': entry['domain'],
                                'type': 'host',
                                'subtype': 'fqdn',
                                'source': 'threatminer'
                            })

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))

        # check for subdomains
        try:
            status, response = get(sub_url)
            if status:
                data = response.json()

                if data['status_code'] == '200' and 'status_message' == 'Results found.':
                    self.artifact['data']['threatminer'] = {'subdomains': data['results']}

                # check for potential children artifacts
                if isinstance(self.artifact['data']['threatminer'], dict):
                    for entry in self.artifact['data']['threatminer']['subdomains']:
                        if detect_type(entry) == 'host':
                            self.artifact['children'].append({
                                'name': entry['domain'],
                                'type': 'host',
                                'subtype': 'fqdn',
                                'source': 'threatminer'
                            })

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))

    def hash(self):
        url = 'https://api.threatminer.org/v2/sample.php?q=%s&rt=3' % self.artifact['name']

        try:
            status, response = get(url)

            if status:
                data = response.json()

                if data['status_code'] == '200' and 'status_message' == 'Results found.':
                    self.artifact['data']['threatminer'] = {'http_traffic': data['results']}

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))

        # there could potentially be a ton of data from this query for files so for now let's avoid
        # creating child artifacts based off the results. example tests show that lots of the traffic
        # is for legitimate domains in some cases.. we dont want to flood the DB with google, etc etc.
        ##
        # example of JSON response for http_traffic of file hash:
        #  {
        #     "status_code": "200",
        #     "status_message": "Results found.",
        #     "results": [{
        #         "domains": [{
        #             "ip": "173.194.192.100",
        #             "domain": "www.google-analytics.com"
        #         }, {
        #             "ip": "173.194.192.97",
        #             "domain": "www.googletagmanager.com"
        #         }, {
        #             "ip": "216.58.216.106",
        #             "domain": "ajax.googleapis.com"
        #         }, {
        #             "ip": "209.222.0.52",
        #             "domain": "www.installaware.com"
        #         }, {
        #             "ip": "72.32.150.153",
        #             "domain": "installaware.app12.hubspot.com"
        #         }, {
        #             "ip": "172.230.212.74",
        #             "domain": "js.hubspot.com"
        #         }, {
        #             "ip": "74.125.135.156",
        #             "domain": "stats.g.doubleclick.net"
        #         }],
        #         "hosts": ["209.222.0.52", "72.32.150.153"]
        #     }]
        # }

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
