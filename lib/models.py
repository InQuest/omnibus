#!/usr/bin/env python
##
# omnibus - deadbits.
# starter data models for host, email, and user artifacts
##

from common import is_ipv4
from common import is_ipv6
from common import is_fqdn

from common import success
from common import warning


class User(object):
    def __init__(self, username, source=''):
        self.data = {}
        self.notes = []
        self.name = username


class Email(object):
    def __init__(self, email_address, source=''):
        self.data = {}
        self.notes = []
        self.name = email_address


class Host(object):
    def __init__(self, host, source=''):
        self.name = host
        self.data = {}
        self.type = None
        self.notes = []
        self.source = source

        if self.type is None:
            self._set_type()


    def _set_type(self):
        if is_ipv4(self.name):
            self.type = 'ipv4'
        elif is_ipv6(self.name):
            self.type = 'ipv6'
        elif is_fqdn(self.name):
            self.type = 'fqdn'
        else:
            warning('host type cannot be determined. must be one of: ipv4, ipv6, fqdn')
            self.type = 'invalid'
        success('set artifact type: %s' % self.type)
