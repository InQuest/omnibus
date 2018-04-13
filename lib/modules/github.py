#!/usr/bin/env python
##
# omnibus - deadbits
# search github for active users
##
from http import http_get

from common import error


def run(username):
    results = None
    url = 'https://api.github.com/users/%s' % username
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        error('failed to get Github results (%s)' % username)
        return results

    if status:
        results = response.json()

    return results


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
