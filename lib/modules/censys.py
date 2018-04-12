#!/usr/bin/env python
##
# omnibus - deadbits.
# censys.io module
##
import censys.ipv4

from common import is_ipv4
from common import get_apikey


def run(host):
    key = get_apikey('censys')
    results = None

    if is_ipv4(host):
        censysio = censys.ipv4.CensysIPv4(api_id=key['token'], api_secret=key['secret'])

        try:
            results = censysio.view(host)
        except:
            return results

    return results
