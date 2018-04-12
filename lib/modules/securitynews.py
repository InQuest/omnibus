#!/usr/bin/env python
##
# omnibus - deadbits.
# cyber security news
##
import xml.etree.ElementTree as ET

from common import http_get


def vuln_news():
    url = "https://news.google.com/news/rss/search/section/q/CVE%20vulnerability/CVE%20vulnerability?hl=en&gl=US&ned=us"
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        return None

    if status:
        result = []
        try:
            content = response.text.encode('utf-8')
            root = ET.fromstring(content)

            for item in root.iter('item'):
                title = item.find('title').text
                link = item.find('link').text
                result.append({'title': title, 'url': link})
        except:
            return None

    return result


def security_news():
    url = 'https://news.google.com/news/rss/search/section/q/cybersecurity/cybersecurity?hl=en&gl=US&ned=us'
    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

    try:
        status, response = http_get(url, headers=headers)
    except:
        return None

    if status:
        result = []
        try:
            content = response.text.encode('utf-8')
            root = ET.fromstring(content)

            for item in root.iter('item'):
                title = item.find('title').text
                link = item.find('link').text
                result.append({'title': title, 'url': link})
        except:
            return None

    return result


def run():
    result = {}
    result['security'] = security_news()
    result['vulnerablities'] = vuln_news()
    return result
