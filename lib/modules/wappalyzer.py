#!/usr/bin/env python
##
# omnibus - deadbits
# Wappalyzer module
##

import warnings

import Wappalyzer

from requests.packages.urllib3 import exceptions

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        if not self.artifact['name'].startwith('https://') or not self.artifact['name'].startwith('http://'):
            warning('Artifact is not a valid URL: pre-pendig "http://" to artifact for this module to run\n \
                    This will be reset after the module executes.')
            self.artifact['name'] = 'http://' + self.artifact['name']

        self.artifact['data']['wappalyzer'] = None


    def run(self):
        # Everybody hating we just call them skids tho
        # In love with the OSINt, I ain't never letting go...
        fetty_wap = Wappalyzer.Wappalyzer

        # build Wappalyzer instance using default applications database
        wap = fetty_wap.latest()

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
            warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)

            target_url = Wappalyzer.WebPage.new_from_url(self.artifact['name'], verify=False)
            result = wap.analyze_with_categories(target_url)

            if result:
                self.artifact['data']['wappalyzer'] = result

            # reset artifact to normal name
            self.artifact['name'] = self.artifact['name'].strip('http://')[1]


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
