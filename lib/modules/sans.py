#!/usr/bin/env python
##
# omnibus - deadbits.
# query SANS ISC API
##
import dshield


def run(host):
    result = None

    try:
        data = dshield.ip(host)
        result = data['ip']
    except:
        pass

    return result


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
