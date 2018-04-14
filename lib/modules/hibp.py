#!/usr/bin/env python
##
# omnibus - deadbits
# haveibeenpwned
##
from http import get

from common import is_email


def check_breaches(account):
    results = None
    url = 'https://haveibeenpwned.com/api/v2/breachedaccount/%s' % account
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = get(url, headers=headers)
    except:
        return results

    if status:
        results = response.json()

    return results


def check_pastes(account):
    results = None
    url = 'https://haveibeenpwned.com/api/v2/pasteaccount/%s' % account
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = get(url, headers=headers)
    except:
        return results

    if status:
        results = response.json()

    return results


def run(account):
    result = {'breaches': None, 'pastes': None}

    result['breaches'] = check_breaches(account)

    if is_email(account):
        result['pastes'] = check_pastes(account)

    return result


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
