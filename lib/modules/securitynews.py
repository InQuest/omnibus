#!/usr/bin/env python
##
# omnibus - deadbits.
# cyber security news
##
import xml.etree.ElementTree as ET

from http import get


class Plugin(object):
    def __init__(self):
        self.results = {'Vulnerabilities': [], 'Security': []}
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def vuln(self):
        url = "https://news.google.com/news/rss/search/section/q/CVE%20vulnerability/CVE%20vulnerability?hl=en&gl=US&ned=us"

        try:
            status, response = get(url, headers=self.headers)
            if status:
                try:
                    content = response.text.encode('utf-8')
                    root = ET.fromstring(content)

                    for item in root.iter('item'):
                        title = item.find('title').text
                        link = item.find('link').text
                        self.results['Vulnerablities'].append({
                            'title': title,
                            'url': link
                        })
                except:
                    pass
        except:
            pass


    def security(self):
        url = 'https://news.google.com/news/rss/search/section/q/cybersecurity/cybersecurity?hl=en&gl=US&ned=us'

        try:
            status, response = get(url, headers=self.headers)
            if status:
                try:
                    content = response.text.encode('utf-8')
                    root = ET.fromstring(content)

                    for item in root.iter('item'):
                        title = item.find('title').text
                        link = item.find('link').text
                        self.results['Security'].append({
                            'title': title,
                            'url': link
                        })
                except:
                    pass
        except:
            pass


    def run(self):
        self.vuln()
        self.security()


def main(artifact):
    plugin = Plugin()
    plugin.run()
    return plugin.results
