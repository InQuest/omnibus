#!/usr/bin/env python
##
# omnibus - deadbits.
# query SANS ISC API
##
import dshield
from common import is_ipv4


def run(host):
    if is_ipv4(host):
        result = None

        try:
            data = dshield.ip(host)
        except:
            return result

        result = data['ip']

    return result
