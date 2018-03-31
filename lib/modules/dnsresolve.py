#!/usr/bin/env python
##
# omnibus - deadbits.
# resolve dns records
##

import dns.resolver


def get_record(domain, record):
    results = []

    try:
        res = dns.resolver.query(domain, record)
        for item in res:
            if item not in results:
                results.append(str(item))
    except:
        results.append(None)

    return results


def run(domain):
    results = {}

    results['A'] = get_record(domain, 'A')
    results['AAAA'] = get_record(domain, 'AAAA')
    results['CNAME'] = get_record(domain, 'CNAME')
    results['NS'] = get_record(domain, 'NS')
    results['MX'] = get_record(domain, 'MX')
    results['TXT'] = get_record(domain, 'TXT')

    return results
