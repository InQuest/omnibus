#!/usr/bin/env pytohn
##
# omnibus - deadbits
# module execution for CLI application
##
import json
import importlib

from pygments import lexers
from pygments import highlight
from pygments import formatters

from common import error
from common import success
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
                'shodan', 'virustotal', 'webserver', 'whois', 'passivetotal'
            ],
            'user': [
                'github', 'gitlab', 'gist', 'keybase',
            ],
            'email': [
                'clearbit', 'fullcontact', 'hackedemails', 'hibp', 'pgp'
            ],
        }


    def machine(self, session, artifact):
        """ Run all modules against an artifact of a given type """
        is_key, value = lookup_key(session, artifact)

        if is_key and value is None:
            error('Unable to find artifact key in session (%s)' % artifact)
            return
        elif is_key and value is not None:
            artifact = value
        else:
            pass

        artifact_type = detect_type(artifact)

        if artifact_type not in self.modules.keys():
            warning('Argument is not a valid artifact (%s)' % artifact)
            return

        modules = self.modules[artifact_type]

        for m in modules:
            module_result = self.run(m, artifact, artifact_type)

            if module_result is not None:
                if self.db.exists(artifact_type, {'name': artifact}):
                    doc_id = self.db.update_one(artifact_type, {'name': artifact}, {'data.' + m: module_result})
                    if doc_id is None:
                        warning('Failed to update Mongo document (%s)' % artifact)

                print(highlight(unicode(json.dumps(module_result, indent=2, default=jsondate), 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter()))

            else:
                warning('Failed to get module results (%s)' % m)

        success('Machine completed')


    def submit(self, session, module, artifact, no_argument=False):
        """ RUn a single module against an artifact """
        if not no_argument:
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
                    module_type = 'ipv4'
                elif is_fqdn(artifact):
                    module_type = 'fqdn'

                if module_type not in self.modules.keys():
                    warning('Argument is not a valid artifact (%s)' % artifact)
                    return

            if artifact_type not in self.modules.keys():
                warning('Argument is not a valid artifact (%s)' % artifact)
                return


            if module not in self.modules[artifact_type]:
                warning('Artifact is not accepted by module (%s) (valid types: %s)' % artifact)
                return

        if artifact_type == 'host':
            module_result = self.run(module, artifact, module_type)
        else:
            module_result = self.run(module, artifact, artifact_type)

        if module_result is not None:
            if not no_argument:
                if self.db.exists(artifact_type, {'name': artifact}):
                    doc_id = self.db.update_one(artifact_type, {'name': artifact}, {'data.' + module: module_result})
                    if doc_id is None:
                        warning('Failed to update Mongo document (%s)' % artifact)

            print(highlight(unicode(json.dumps(module_result, indent=2, default=jsondate), 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter()))

        else:
            warning('Failed to get module results (%s)' % module)


    def run(self, module, artifact, artifact_type):
        """ Load Python library from modules directory and execute main function """
        results = None

        try:
            ptr = importlib.import_module('lib.modules.%s' % module)
        except Exception as err:
            error('Failed to load module (%s)' % module)
            raise err

        try:
            results = ptr.main(artifact, artifact_type)
        except Exception as err:
            error('Exception caught when running module (%s)' % module)
            raise err

        return results
