#!/usr/bin/env python
##
# omnibus - deadbits.
# export artifacts to an arbitrary HTTP API endpoint
##
import simplejson

from http import post

from common import success
from common import warning


class Export(object):
    def __init__(self, artifacts=None, url=None, params=None, headers=None):
        self.url = url
        self.artifacts = artifacts
        self.params = params
        self.result = None

        self.headers = {
            'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/omnibus',
            'Content-Type': 'application/json'
        }

        if headers is not None:
            self.headers.update(headers)


    def send(self):
        """ Send all artifacts to provided HTTP endpoint as JSON """
        if self.params is not None:
            status, response = post(self.url,
                headers=self.headers,
                params=self.params,
                json=simplejson.dumps(self.artifacts))
        else:
            status, response = post(self.url,
                headers=self.headers,
                json=simplejson.dumps(self.artifacts))

        if not status:
            warning('Failed to export artifacts (HTTP Endpoint: %s)' % self.url)
        else:
            success('Successfully export artifacts (HTTP Endpoint: %s) (Artifacts: %d)' % (self.url, len(self.artifacts)))
