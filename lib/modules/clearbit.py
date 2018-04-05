#!/usr/bin/env python
##
# omnibus - deadbits.
# clearbit email lookup module
##
import json

from common import http_get
from common import error
from common import warning
from common import get_apikey


def run(email_address):
    api_key = get_apikey('clearbit')
    headers = {'Authorization': 'Bearer %s' % api_key}
    results = {}

    resp = http_get('https://person.clearbit.com/v1/people/email/%s' % email_address,
            headers=headers)

    if resp[0] is False:
        error('failed to get Clearbit API results: %s' % email_address)
        return None

    if 'error' in resp[1].content and 'queued' in resp[1].content:
        warning('results are queued by Clearbit. please re-run module after 5-10 minutes.')
        return None

    results = json.loads(resp[1].content)
    return results
