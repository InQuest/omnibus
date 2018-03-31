#!/usr/bin/env python
##
# omnibus - deadbits.
# whois module
##
from ipwhois import IPWhois


def run(host):
    results = {}
    whois = IPWhois(host)

    try:
        data = whois.lookup_rdap(depth=1)
    except:
        data = None

    if data is not None:
        results['ASN'] = data['asn']
        results['Organization'] = data['network']['name'] if 'network' in data.keys() else None
        results['CIDR'] = data['network']['cidr'] if 'network' in data.keys() else None
        results['Country'] = data['network']['country'] if 'network' in data.keys() else None

    return results
