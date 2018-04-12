#!/usr/bin/env python
##
# omnibus - deadbits.
# whois module
##
from whois import whois
from ipwhois import IPWhois


def host_run(host):
    results = None

    try:
        results = whois(host)
    except:
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
