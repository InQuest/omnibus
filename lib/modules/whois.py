#!/usr/bin/env python
##
# omnibus - deadbits.
# whois module
##
import whois

from ipwhois import IPWhois


def fqdn_run(host):
    results = None

    try:
        results = whois.whois(host)
    except Exception as err:
        raise err
        return results

    return results


def ip_run(host):
    results = None
    whois = IPWhois(host)

    try:
        data = whois.lookup_rdap(depth=1)
    except:
        return results

    results = {}
    if data is not None:
        results['ASN'] = data['asn']
        results['Organization'] = data['network']['name'] if 'network' in data.keys() else None
        results['CIDR'] = data['network']['cidr'] if 'network' in data.keys() else None
        results['Country'] = data['network']['country'] if 'network' in data.keys() else None

    return results


def main(artifact, artifact_type=None):
    if artifact_type == 'ipv4':
        result = ip_run(artifact)
    elif artifact_type == 'fqdn':
        result = fqdn_run(artifact)
    else:
        print('returning None')
        return None

    return result
