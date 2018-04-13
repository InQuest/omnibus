#!/usr/bin/env python
##
# omnibus - deadbits.
# cymon.io module
##
import cymon

from common import get_apikey


def ip_run(ip):
    result = None
    key = get_apikey('cymon')

    api = cymon.Cymon(key)

    try:
        result = api.ip_lookup(ip)
    except:
        pass

    return result


def fqdn_run(host):
    result = None
    key = get_apikey('cymon')

    api = cymon.Cymon(key)

    try:
        result = api.domain_lookup(host)
    except:
        pass

    return result


def main(artifact, artifact_type=None):
    if artifact_type == 'ipv4':
        result = ip_run(artifact)
    elif artifact_type == 'fqdn':
        result = fqdn_run(artifact)
    else:
        return None

    return result
