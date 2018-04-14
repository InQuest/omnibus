#!/usr/bin/env python
##
# omnibus - deadbits
# pgp search
##
import re

from BeautifulSoup import BeautifulSoup

from http import get

from common import re_email


def fqdn_run(host):
    result = None
    url = 'http://pgp.mit.edu/pks/lookup?op=index&search=%s' % host
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = get(url, headers=headers)

        result = []
        if status:
            if 'No resuls found' in response.text:
                return result

            data = BeautifulSoup(response.text)
            items = data.fetch('a')
            for item in items:
                matches = re.findall(re_email, item)
                for m in matches:
                    result.append(m)

    except:
        pass

    return result


def email_run(addr):
    result = None
    url = 'http://pgp.mit.edu/pks/lookup?op=index&search=%s' % addr
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = get(url, headers=headers)

        result = []
        if status:
            if 'No resuls found' in response.text:
                return result

            data = BeautifulSoup(response.text)
            hrefs = data.fetch('a')

            for href in hrefs:
                content = href.contents

                if addr in content[0]:
                    try:
                        name = content[0].split('&lt;')[0]
                        result.append(name)
                    except IndexError:
                        pass

    except:
        pass


def main(artifact, artifact_type=None):
    if artifact_type == 'email':
        result = email_run(artifact)
    elif artifact_type == 'fqdn':
        result = fqdn_run(artifact)
    return result
