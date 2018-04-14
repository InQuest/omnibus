#!/usr/bin/env python
##
# omnibus - deadbits
# rss feed reader
##

import feedparser


def run(feed_url):
    result = None

    try:
        feed = feedparser.parse(feed_url)
        result = []
        for idx, item in enumerate(feed['entries']):
            if idx == 19:
                break

    except:
        return result

