#!/usr/bin/env python
##
# omnibus - deadbits.
# virustotal module
##
import requests

from common import is_ipv4
from common import is_fqdn

from common import get_apikey


def run_ip(ip):
    if not is_ipv4(ip):
        return None

    vt_api = get_apikey('virustotal')
    url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    parameters = {'ip': ip, 'apikey': vt_api}
    response = requests.get(url, params=parameters)
    try:
        return response.json()
    except ValueError:
        return None


def run_host(domain):
    if not is_fqdn(domain):
        return None

    vt_api = get_apikey('virustotal')
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'
    parameters = {'domain': domain, 'apikey': vt_api}
    response = requests.get(url, params=parameters)
    try:
        return response.json()
    except ValueError:
        return None
