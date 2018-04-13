#!/usr/bin/env python
##
# omnibus - deadbits.
# virustotal module
##
from http import get

from common import is_hash
from common import is_ipv4
from common import is_fqdn
from common import get_apikey


def run_ip(ip):
    result = None
    vt_api = get_apikey('virustotal')
    parameters = {'ip': ip, 'apikey': vt_api}
    url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'

    if not is_ipv4(ip):
        return None

    try:
        status, response = get(url, params=parameters)
    except:
        return result

    if status:
        data = response.json()
        if data['response_code'] == 1:
            result = data

    return result



def run_fqdn(domain):
    result = None
    vt_api = get_apikey('virustotal')
    parameters = {'domain': domain, 'apikey': vt_api}
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'

    if not is_fqdn(domain):
        return None

    try:
        status, response = get(url, params=parameters)
    except:
        return result

    if status:
        data = response.json()
        if data['response_code'] == 1:
            result = data

    return result


def run_hash(file_hash):
    result = None
    vt_api = get_apikey('virustotal')
    parameters = {'resource': file_hash, 'apikey': vt_api}
    url = 'https://www.virustotal.com/vtapi/v2/file/report'

    if not is_hash(file_hash):
        return None

    try:
        status, response = get(url, params=parameters)
    except:
        return result

    if status:
        data = response.json()
        if data['response_code'] == 1:
            result = data

    return result


def main(artifact, artifact_type=None):
    if artifact_type == 'hash':
        result = run_hash(artifact)
    elif artifact_type == 'ipv4':
        result = run_ip(artifact)
    elif artifact_type == 'fqdn':
        result = run_fqdn(artifact)
    else:
        return None

    return result
