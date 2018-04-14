#!/usr/bin/env python
##
# omnibus - deadbits.
# threatcrowd module
##
import threatcrowd


def run_ip(ip):
    result = None

    try:
        result = threatcrowd.ip_report(ip)
    except:
        pass

    return result


def run_fqdn(domain):
    result = None

    try:
        result = threatcrowd.domain_report(domain)
    except:
        pass

    return result


def main(artifact, artifact_type=None):
    if artifact_type == 'ipv4':
        result = run_ip(artifact)
    elif artifact_type == 'fqdn':
        result = run_fqdn(artifact)
    else:
        return None

    return result
