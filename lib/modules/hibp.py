#!/usr/bin/env python
##
# omnibus - deadbits
# haveibeenpwned
##
from http import get

from common import warning


def run(email_addr):
    results = None
    url = 'https://haveibeenpwned.com/api/v1/breachedaccount/%s' % email_addr
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = get(url, headers=headers)
    except:
        return results

    if status:
        if 'Attention Required! | CloudFlare' in response.content:
            warning('CloudFlare detected; please try module again later.')
        else:
            results = response.json()

    return results


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
