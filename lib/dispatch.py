#!/usr/bin/env pytohn
##
# omnibus - deadbits
# module execution for CLI application
##
import importlib

from common import info
from common import error
from common import success
from common import warning

from common import lookup_key
from common import detect_type

from models import create_artifact


class Dispatch(object):
    def __init__(self, db):
        self.db = db
        self.modules = {
            'btc': [
                'blockchain'
            ],
            'hash': [
                'csirtg', 'malcode', 'mdl', 'otx', 'virustotal', 'threatcrowd', 'threatexpert'
            ],
            'ipv4': [
                'csirtg', 'censys', 'dnsresolve', 'geoip', 'ipinfo', 'ipvoid', 'nmap',
                'sans', 'shodan', 'virustotal', 'threatcrowd', 'passivetotal', 'he', 'otx',
                'whois'
            ],
            'fqdn': [
                'csirtg', 'dnsresolve', 'geoip', 'ipvoid', 'nmap',
                'shodan', 'virustotal', 'passivetotal', 'threatcrowd', 'he', 'otx',
                'whois'
            ],
            'user': [
                'github', 'gitlab', 'gist', 'keybase',
            ],
            'email': [
                'clearbit', 'fullcontact', 'hackedemails', 'hibp', 'pgp', 'whoismind'
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

        artifact = self.db.find(artifact_type, {'name': artifact}, one=True)

        for key in self.modules.keys():
            if artifact['type'] == key:
                modules = self.modules[artifact['type']]
            elif artifact['subtype'] == key:
                modules = self.modules[artifact['subtype']]

        results = []

        for m in modules:
            result = self.run(m, artifact)

            if m in result['data'].keys():
                if result['data'][m] is not None:
                    if self.db.exists(artifact['type'], {'name': artifact['name']}):

                        for child in result['children']:
                            child_artifact = create_artifact(child['name'], parent=artifact['name'],
                                _type=child['type'], source=child['source'], subtype=child['subtype'])

                            if not self.db.exists(child['type'], {'name': child['name']}):
                                self.db.insert_one(child['type'], child_artifact)

                        self.db.update_one(artifact['type'], {'name': artifact['name']}, result)
                        if len(result['children']) > 0:
                            info('Created child artifacts: %d' % len(result['children']))

                    results.append({'[%s]' % m: result['data'][m]})

                else:
                    warning('No results found (%s)' % m)

            else:
                warning('Failed to get module results (%s)' % m)

        success('Machine completed')


    def submit(self, session, module, artifact, no_argument=False):
        """ Run a single module against an artifact """
        if no_argument:
            module_result = self.run(module, None)
            return module_result

        is_key, value = lookup_key(session, artifact)

        if is_key and value is None:
            error('Unable to find artifact key in session (%s)' % artifact)
            return
        elif is_key and value is not None:
            artifact = value
        else:
            pass

        artifact_type = detect_type(artifact)

        artifact = self.db.find(artifact_type, {'name': artifact}, one=True)

        if artifact is None:
            warning('Unable to find artifact in database (%s)' % artifact['name'])
            return None

            if module in self.modules[artifact['type']] or module in self.modules[artifact['subtype']]:
                pass
            else:
                warning('Artifact is not supported by module (%s)' % (artifact['name']))
                return None

        result = self.run(module, artifact)

        if module in result['data'].keys():
            if result['data'][module] is not None:
                if self.db.exists(artifact['type'], {'name': artifact['name']}):

                    for child in result['children']:
                        child_artifact = create_artifact(child['name'], parent=artifact['name'],
                            _type=child['type'], source=child['source'], subtype=child['subtype'])

                        if not self.db.exists(child['type'], {'name': child['name']}):
                            self.db.insert_one(child['type'], child_artifact)

                    self.db.update_one(artifact['type'], {'name': artifact['name']}, result)

                    if len(result['children']) > 0:
                        info('Created child artifacts: %d' % len(result['children']))

                return result['data'][module]

            else:
                warning('No results found (%s)' % module)
                return None

        else:
            warning('Failed to get module results (%s)' % module)


    def run(self, module, artifact):
        """ Load Python library from modules directory and execute main function """
        results = None

        try:
            ptr = importlib.import_module('lib.modules.%s' % module)
        except Exception as err:
            error('Failed to load module (%s)' % module)
            raise err

        try:
            results = ptr.main(artifact)
        except Exception as err:
            error('Exception caught when running module (%s)' % module)
            raise err

        return results
