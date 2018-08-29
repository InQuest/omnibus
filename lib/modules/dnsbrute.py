#!/usr/bin/env python
##
# omnibus - deadbits.
# DNS subdomain discovery
# - limited to VirusTotal searches for now
# - planning to add true word based brute-forcing, and a few other
#   services like dnstrails, dnsdumpster,
##

import requests

from OTXv2 import OTXv2
import IndicatorTypes

from common import get_apikey
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['dnsbrute'] = {}
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

        self.vt_api_key = get_apikey('virustotal')
        if self.vt_api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')

        self.otx_api_key = get_apikey('otx')
        if self.otx_api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')


    def otx(self):
        otx_server = 'https://otx.alienvault.com/'
        otx_conn = OTXv2(self.otx_api_key, server=otx_server)

        domains = []

        try:
            query = otx_conn.get_indicator_details_full(IndicatorTypes.DOMAIN, self.artifact['name'])
            domain_info = query['url_list']['url_list']

            for item in domain_info:
                if item['hostname'] not in domains:
                    domains.append(item['hostname'])

        except Exception as err:
            warning('Caught unknown exception: %s' % str(err))

        self.artifact['data']['dnsbrute']['otx'] = domains


    def vt(self):
        url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        params = {'domain': self.artifact['name'], 'apikey': self.api_key}

        try:
            status, response = requests.get(url, params=params, headers=self.headers)

            if status:
                jdata = response.json()
                self.artifact['data']['dnsbrute']['virustotal'] = jdata['subdomains']

        except Exception as err:
            warning('Caught unknown exception: %s' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
