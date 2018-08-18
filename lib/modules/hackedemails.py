#!/usr/bin/env python
##
# omnibus - deadbits
# hacked-emails.com
##
from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['hackedemails'] = None


    def run(self):
        url = 'https://hacked-emails.com/api?q=%s' % self.artifact['name']
        headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

        try:
            status, response = get(url, headers=headers)

            if status:
                results = response.json()
                self.artifact['data']['hackedemails'] = results
        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
