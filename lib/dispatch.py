#!/usr/bin/env pytohn
##
# omnibus - deadbits
# module execution for CLI application
##
import json
import importlib

from common import error
from common import warning

from common import is_ipv4
from common import is_fqdn

from common import jsondate
from common import lookup_key
from common import detect_type


class Dispatch(object):
    def __init__(self, db):
        self.db = db
        self.modules = {
            'btc': [
                'blockchain'
            ],
            'hash': [
                'malcode', 'mdl', 'otx', 'virustotal'
            ],
            'ipv4': [
                'censys', 'cymon', 'dnsresolve', 'geoip', 'ipinfo', 'ipvoid', 'nmap', 'projecthp',
                'sans', 'shodan', 'virustotal', 'webserver', 'whois'
            ],
            'fqdn': [
                'cymon', 'dnsbrute', 'dnsresolve', 'geoip', 'ipinfo', 'ipvoid', 'nmap', 'projecthp',
                'shodan', 'virustotal', 'webserver', 'whois'
            ],
            'user': [
                'github', 'gitlab', 'gist', 'keybase',
            ],
            'email': [
                'clearbit', 'fullcontact', 'hackedemails', 'hibp', 'pgp'
            ],
        }


    def submit(self, session, module, artifact):
        is_key, value = lookup_key(session, artifact)

        if is_key and value is None:
            error('Unable to find artifact key in session (%s)' % artifact)
            return
        elif is_key and value is not None:
            artifact = value
        else:
            pass

        artifact_type = detect_type(artifact)

        if artifact_type == 'host':
            if is_ipv4(artifact):
                artifact_type = 'ipv4'
            elif is_fqdn(artifact):
                artifact_type = 'fqdn'

        if artifact_type not in self.modules.keys():
            warning('Argument is not a valid artifact (%s)' % artifact)
            return

        if module not in self.modules[artifact_type]:
            warning('Artifact is not accepted by module (%s) (valid types: %s)' % artifact)
            return

        module_result = self.run(module, artifact, artifact_type)

        if module_result is not None:
            if self.db.exists(artifact_type, {'name': artifact}):
                doc_id = self.db.update(artifact_type, {'name': artifact}, {'data.' + module: module_result})
                if doc_id is None:
                    warning('Failed to update Mongo document (%s)' % artifact)

            print(json.dumps(module_result, indent=2, default=jsondate))

        else:
            warning('Failed to get module results (%s)' % module)


    def run(self, module, artifact, artifact_type):
        results = None

        try:
            ptr = importlib.import_module('lib.modules.%s' % module)
            print(ptr)
        except Exception as err:
            error('Failed to load module (%s)' % module)
            raise err

        try:
            results = ptr.main(artifact, artifact_type)
        except Exception as err:
            error('Exception caught when running module (%s)' % module)
            raise err

        return results
