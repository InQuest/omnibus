#!/usr/bin/env python
##
# omnibus - deadbits.
# yara file scanner
##

import os
import yara

from common import list_dir
from common import get_option

from constants import root_path


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['yara'] = None

        cfg_rules = get_option('modules', 'yara_rules')
        if cfg_rules == '':
            raise TypeError('Invalid YARA rules directory in conf file: Cannot be empty!')

        self.rules = os.path.join(root_path, 'etc', cfg_rules)
        if list_dir(self.rules) == 0:
            raise TypeError('Invalid YARA rules directory in conf file: No files contained in directory!')


    def run(self):
        results = {'matches': {}}

        all_rules = list_dir(self.rules)

        for r in all_rules:
            rule = yara.compile(r)
            matches = rule.match(data=open(self.artifact['path'], 'rb').read())

            for m in matches:
                if m.rule not in results['matches'].keys():
                    results['matches'][m.rule] = []
                for tag in m.tags:
                    if tag not in results['matches'][m.rule]:
                        results['matches'][m.rule].append(tag)

        self.artifact['data']['yara'] = results


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
