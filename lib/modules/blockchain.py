#!/usr/bin/env python
##
# omnibus - deadbits
# blockchain.info address lookup
##
from http import get


def run(btc_addr):
    result = None
    url = 'https://blockchain.info/rawaddr/%s' % btc_addr
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = get(url, headers=headers)
        if status:
            result = response.json()
    except:
        pass

    return result


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
