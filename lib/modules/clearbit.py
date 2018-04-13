#!/usr/bin/env python
##
# omnibus - deadbits.
# clearbit email lookup module
##
import json

from http import get

from common import warning
from common import get_apikey


def run(email_address):
    result = None
    api_key = get_apikey('clearbit')
    url = 'https://person.clearbit.com/v1/people/email/%s' % email_address
    headers = {
        'Authorization': 'Bearer %s' % api_key,
        'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'
    }

    try:
        status, response = get(url, headers=headers)
    except:
        return result

    if status:
        if 'error' in response.content and 'queued' in response.content:
            warning('results are queued by Clearbit. please re-run module after 5-10 minutes.')
            return result

        result = json.loads(response.content)

    return result


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
