#!/usr/bin/env python
##
# omnibus - deadbits.
# censys.io module
##
import censys.ipv4

from common import is_ipv4
from common import get_apikey


def run(domain):
    key = get_apikey('censys')

    if is_ipv4(domain):
        censysio = censys.ipv4.CensysIPv4(api_id=key['token'], api_secret=key['secret'])

        try:
            results = censysio.view(domain)
        except:
            results = {}

    else:
        results = {}

    return results
