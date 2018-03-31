#!/usr/bin/env python
##
# omnibus - deadbits.
# clearbit email lookup module
##
import json
import requests

from common import error
from common import warning
from common import get_apikey


def run(email_address):
    api_key = get_apikey('clearbit')
    headers = {'Authorization': 'Bearer %s' % api_key}
    results = {}

    try:
        resp = requests.get('https://person.clearbit.com/v1/people/email/%s' % email_address,
            headers=headers)
    except:
        error('failed to get Clearbit API results: %s' % email_address)
        return results

    if 'error' in resp.content and 'queued' in resp.content:
        warning('results are queued by Clearbit. please re-run module after 5-10 minutes.')
        return results

    results = json.loads(resp.content)
    return results
