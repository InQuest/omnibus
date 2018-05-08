#!/usr/bin/env python
##
# omnibus - deadbits.
# starter data models for host, email, and user artifacts
##

from common import is_ipv4
from common import is_ipv6
from common import is_fqdn
from common import is_hash

from common import warning

from common import timestamp
from common import detect_type


artifact_types = ['host', 'email', 'user', 'bitcoin', 'hash']


class Artifact(object):
    def __init__(self, name, type, source=None, subtype=None, case_id=None):
        self.name = name
        self.created = timestamp()
        self.type = type
        self.subtype = subtype
        self.source = source
        self.parent = None
        self.children = []
        self.case_id = case_id
        self.tags = []
        self.notes = []
        self.data = {}

        if self.type == 'host':
            if is_ipv4(self.name):
                self.subtype = 'ipv4'
            elif is_ipv6(self.name):
                self.subtype = 'ipv6'
            elif is_fqdn(self.name):
                self.subtype = 'fqdn'
            else:
                warning('host type cannot be determined. must be one of: ipv4, ipv6, fqdn')
                self.subtype = 'unknown'

        elif self.type == 'hash':
            result = is_hash(self.name)
            if result is None:
                warning('hash is not a valid md5, sha1, sha256, or sha512')
                self.subtype = 'unknown'
            else:
                self.subtype = result


def create_artifact(artifact_name, _type=None, source=None, subtype=None, parent=None):
    if _type is None:
        artifact_type = detect_type(artifact_name)
    else:
        artifact_type = _type

    if artifact_type not in artifact_types:
        warning('Artifact must be one of: email, ipv4, fqdn, user, hash, bitcoin address')
        return None

    created = Artifact(name=artifact_name, type=artifact_type, subtype=subtype, source=source)

    if parent is not None:
        created.parent = parent

    return created
