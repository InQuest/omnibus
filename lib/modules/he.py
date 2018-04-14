#!/usr/bin/env python
##
# omnibus - deadbits
# hurricane eletric
##
import re

from BeautifulSoup import BeautifulSoup

from http import get


def ip_run(ip):
    result = None
    url = 'http://bgp.he.net/ip/%s#_dns' % ip
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = get(url, headers=headers)

        if status:
            result = []
            data = BeautifulSoup(response.text)

            for item in data.findAll(attrs={'id': 'dns', 'class': 'tabdata hidden'}):
                result.append(item.text.strip())

    except:
        pass

    return result


def fqdn_run(host):
    result = None
    url = 'http://bgp.he.net/dns/%s#_whois' % host
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = get(url, headers=headers)

        result = []
        if status:
            pattern = re.compile('\/dns\/.+\".title\=\".+\"\>(.+)<\/a\>', re.IGNORECASE)
            hosts = re.findall(pattern, response.text)
            for h in hosts:
                result.append(h.strip())

    except:
        pass

    return result


def main(artifact, artifact_type=None):
    if artifact_type == 'ipv4':
        result = ip_run(artifact)
    elif artifact_type == 'fqdn':
        result = fqdn_run(artifact)

    return result
