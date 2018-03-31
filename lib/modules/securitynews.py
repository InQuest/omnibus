#!/usr/bin/env python
##
# omnibus - deadbits.
# cyber security news
##
import requests
import xml.etree.ElementTree as ET


def vuln_news():
    result = []
    urlip = "https://news.google.com/news/rss/search/section/q/CVE%20vulnerability/CVE%20vulnerability?hl=en&gl=US&ned=us"

    try:
        resp = requests.get(urlip)
        content = resp.text.encode('utf-8')
        root = ET.fromstring(content)

        for item in root.iter('item'):
            title = item.find('title').text
            link = item.find('link').text
            result.append({'title': title, 'url': link})

    except:
        return None


def security_news():
    result = []
    url = 'https://news.google.com/news/rss/search/section/q/cybersecurity/cybersecurity?hl=en&gl=US&ned=us'

    try:
        resp = requests.get(url)
        content = resp.text.encode('utf-8')
        root = ET.fromstring(content)

        for item in root.iter('item'):
            title = item.find('title').text
            link = item.find('link').text
            result.append({'title': title, 'url': link})

    except:
        return None


def run():
    result = {}
    result['security'] = security_news()
    result['vulnerablities'] = vuln_news()
    return result
