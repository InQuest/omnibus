#!/usr/bin/env python
##
# omnibus - deadbits.
# dns sub-domain brute force module
##
import BeautifulSoup

from common import http_get


def run(email_addr):
    result = None
    url = 'http://www.whoismind.com/emails/%s.html' % email_addr
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        return result

    if status:
        result = []

        content = BeautifulSoup(response.content, 'lxml')
        a_tag = content.findAll('a')
        for tag in a_tag:
            if tag.text in tag['href'] and tag.text not in result:
                result.append(tag.text)

    return result
