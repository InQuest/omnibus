#!/usr/bin/env python
##
# omnibus - deadbits
# rss feed reader
##

import feedparser

from common import warning


class Plugin(object):
    def __init__(self, feed_url):
        self.url = feed_url
        self.results = []


    def run(self):
        try:
            feed = feedparser.parse(self.url)

            for idx, item in enumerate(feed['entries']):
                if idx == 19:
                    break

                else:
                    self.results.append({
                        'url': item['url'],
                        'title': item['title']
                    })

        except Exception as err:
            warning('Caught exception in module (%s)' % str(err))



def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.results
