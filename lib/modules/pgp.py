#!/usr/bin/env python
##
# omnibus - deadbits
# pgp search
##
import re

from BeautifulSoup import BeautifulSoup

from http import get

from common import re_email
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['pgp'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def fqdn(self):
        url = 'http://pgp.mit.edu/pks/lookup?op=index&search=%s' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)

            if status:
                if 'No results found' in response.text:
                    pass

                else:
                    data = BeautifulSoup(response.text)
                    items = data.fetch('a')
                    for item in items:
                        matches = re.findall(re_email, item)
                        for m in matches:
                            if isinstance(self.artifact['data']['pgp'], list):
                                self.artifact['data']['pgp'].append(m)
                            else:
                                self.artifact['data']['pgp'] = []
                                self.artifact['data']['pgp'].append(m)

                            self.artifact['children'].append({
                                'name': m,
                                'type': 'email',
                                'source': 'PGP',
                                'subtype': None})

        except:
            pass


    def email(self):
        url = 'http://pgp.mit.edu/pks/lookup?op=index&search=%s' % self.artifact['name']

        try:
            status, response = get(url, headers=self.headers)

            if status:
                if 'No results found' in response.text:
                    pass
                else:
                    data = BeautifulSoup(response.text)
                    hrefs = data.fetch('a')

                    for href in hrefs:
                        content = href.contents

                        if self.artifact['name'] in content[0]:
                            try:
                                name = content[0].split('&lt;')[0]
                                if isinstance(self.artifact['data']['pgp'], list):
                                    self.artifact['data']['pgp'].append(name)
                                else:
                                    self.artifact['data']['pgp'] = []
                                    self.artifact['data']['pgp'].append(name)
                            except IndexError:
                                pass

        except:
            pass


    def run(self):
        if self.artifact['type'] == 'email':
            self.email()
        elif self.artifact['type'] == 'fqdn':
            self.fqdn()
        else:
            warning('PGP module only accepts artifact types email or fqdn')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
