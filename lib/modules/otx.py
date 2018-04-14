#!/usr/bin/env python
##
# omnibus - deadbits.
# alienvault otx module
##
from http import get


def ip_run(ip):
    result = None
    url = 'https://otx.alienvault.com:443/api/v1/indicators/IPv4/%s/' % ip

    try:
        status, response = get(url)

        if status:
            result = response.json()
    except:
        pass

    return result


def fqdn_run(ip):
    result = None
    url = 'https://otx.alienvault.com:443/api/v1/indicators/domain/%s/' % ip

    try:
        status, response = get(url)

        if status:
            result = response.json()
    except:
        pass

    return result


def hash_run(ip):
    result = None
    url = 'https://otx.alienvault.com:443/api/v1/indicators/file/%s/' % ip

    try:
        status, response = get(url)

        if status:
            result = response.json()
    except:
        pass

    return result


def main(artifact, artifact_type=None):
    if artifact_type == 'hash':
        result = hash_run(artifact)
    elif artifact_type == 'ipv4':
        result = ip_run(artifact)
    elif artifact_type == 'fqdn':
        result = fqdn_run(artifact)
    else:
        return None

    return result
