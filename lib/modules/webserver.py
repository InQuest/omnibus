#!/usr/bin/env python
##
# omnibus - deadbits
# webserver fingerprinting module
##
import os

import grequests

import warnings

import Wappalyzer

from requests.packages.urllib3 import exceptions

from common import running
from common import warning
from common import get_option


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        if not self.artifact['name'].startwith('https://') or not self.artifact['name'].startwith('http://'):
            warning('Artifact is not a valid URL: temporarily prepending "http://" to artifact for this modules execution.')
            self.artifact['name'] = 'http://' + self.artifact['name']

        self.artifact['data']['webserver'] = None

        self.do_brute = True
        self.dir_list = get_option('modules', 'web_dir_list')
        if self.dir_list != '':
            if not os.path.exists(self.dir_list):
                warning('Directory brute force will not run. Directory list file not found on disk. (%s)' % self.dir_list)
                self.do_brute = False
        else:
            self.do_brute = False


    def wapp(self):
        # Everybody hating we just call them skids tho
        # In love with the OSINt, I ain't never letting go...
        fetty_wap = Wappalyzer.Wappalyzer

        # build Wappalyzer instance using default applications database
        wap = fetty_wap.latest()

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
            warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)

            target_url = Wappalyzer.WebPage.new_from_url(self.artifact['name'], verify=False)
            result = wap.analyze(target_url)

            if result:
                self.artifact['data']['webserver']['running'] = list(result)


    def dirbrute(self):
        results = []

        urls = []
        for line in open(self.dir_list, 'rb').readlines():
            urls.append(line.rstrip('\n'))

        reqs = (grequests.get(url) for url in urls)
        resps = reqs.map(reqs)
        for resp in resps:
            if resp.status_code != 404:
                results.append({resp.url: resp.status_code})

        self.artifact['data']['webserver']['directories'] = results


    def run(self):
        if self.do_brute:
            running('Starting directory brute force ...')
            self.dirbrute()

        running('Analyzing running software ...')
        self.wapp()




def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
