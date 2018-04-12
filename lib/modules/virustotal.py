#!/usr/bin/env python
##
# omnibus - deadbits.
# virustotal module
##

from common import is_ipv4
from common import is_fqdn
from common import http_get
from common import get_apikey


def run_ip(ip):
    result = None
    vt_api = get_apikey('virustotal')
    parameters = {'ip': ip, 'apikey': vt_api}
    url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'

    if not is_ipv4(ip):
        return None

    try:
        status, response = http_get(url, params=parameters)
    except:
        return result

    if status:
        result = response.json()

    return result



def run_host(domain):
    result = None
    vt_api = get_apikey('virustotal')
    parameters = {'domain': domain, 'apikey': vt_api}
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'

    if not is_fqdn(domain):
        return None

    try:
        status, response = http_get(url, params=parameters)
    except:
        return result

    if status:
        result = response.json()

    return result
