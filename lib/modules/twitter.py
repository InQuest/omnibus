#!/usr/bin/env python
##
# omnibus - deadbits
# Twitter username search
##

from BeautifulSoup import BeautifulSoup

from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['twitter'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def run(self):
        url = 'https://www.twitter.com/%s' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)

            if status:
                soup = BeautifulSoup(response.content, 'lxml')

                self.artifact['data']['twitter'] = {}
                self.artifact['data']['twitter']['name'] = soup.find('h1').contents[1].text

                try:
                    self.artifact['data']['twitter']['location'] = soup.find('span', class_='ProfileHeaderCard-locationText u-dir').contents[1].text
                except:
                    self.artifact['data']['twitter']['location'] = None

                self.artifact['data']['twitter']['description'] = soup.find('div', class_='ProfileHeaderCard').contents[5].text
                self.artifact['data']['twitter']['created'] = soup.find('div', class_='ProfileHeaderCard-joinDate').contents[3].text

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
