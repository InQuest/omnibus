#!/usr/bin/env python
##
# omnibus - deadbits.
# HTTP requests library
##
import requests
import warnings

from requests.packages.urllib3 import exceptions


def http_post(*args, **kwargs):
    """ Wrapped to silently ignore certain warnings from urllib3 library """
    kwargs['verify'] = False
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
        warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)
        try:
            req = requests.get(*args, **kwargs)
        except:
            return (False, None)

        if req.status_code == 200:
            return (True, req)
        else:
            return (False, req)


def http_get(*args, **kwargs):
    """ Wrapped to silently ignore certain warnings from urllib3 library """
    kwargs['verify'] = False
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
        warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)
        try:
            req = requests.get(*args, **kwargs)
        except:
            return (False, None)

        if req.status_code == 200:
            return (True, req)
        else:
            return (False, req)
