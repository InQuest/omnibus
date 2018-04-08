#!/usr/bin/env python
##
# omnibus - deadbits.
# clearbit email lookup module
##
import json

from common import http_get
from common import error
from common import warning
from common import http_get
from common import get_apikey


def run(email_address):
    results = None
    api_key = get_apikey('clearbit')
    url = 'https://person.clearbit.com/v1/people/email/%s' % email_address
    headers = {
        'Authorization': 'Bearer %s' % api_key,
        'User-Agent': 'OSINT Omnibus (https://github.com/deadbits/omnibus)'
    }

    try:
        status, response = http_get(url, headers=headers)
    except:
        error('failed to get Clearbit results (%s)' % email_address)
        return results

    if status:
        if 'error' in response.content and 'queued' in response.content:
            warning('results are queued by Clearbit. please re-run module after 5-10 minutes.')
            return results

        results = json.loads(response.content)

    return results
