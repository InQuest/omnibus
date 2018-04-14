#!/usr/bin/env python
##
# omnibus - deadbits
# fullcontact.com
##
from http import get

from common import get_apikey


def run(email_addr):
    result = None
    key = get_apikey('fullcontact')
    headers = {
        'X-FullContact-APIKey': key,
        'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'
    }

    try:
        status, response = get('https://api.fullcontact.com/v2/person.json?email=%s' % email_addr,
            headers=headers)

        if status:
            result = response.json()
    except:
        pass

    return result


def main(artifact, artifact_type):
    result = run(artifact)
    return result
