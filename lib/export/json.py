#!/usr/bin/env python
##
# omnibus - deadbits.
# export artifacts to a local JSON file
##
import os
import json

from common import timestamp

from common import error
from common import success
from common import warning


class Export(object):
    def __init__(self, artifacts=None, file_path=None, file_name='report.json'):
        self.artifacts = artifacts
        self.file_path = file_path

        self.file_name = '%s_report.json' % timestamp

        if file_path:
            self.set_filepath(file_path, file_name)


    def set_filepath(self, file_path, file_name):
        if os.path.isdir(file_path):
            self.file_path = os.path.join(file_path, file_name)

            if not os.path.exists(self.file_path):
                self.send()
                success('Saved report to %s' % self.file_path)
                return True

            return False

        else:
            error('Unable to find directory %s - cannot save report' % file_path)
            return False


    def send(self):
        """ Send all artifacts to local JSON file and save """
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            warning('Existing file path is not empty. Please provide a new or empty file (%s)' % self.file_path)
            return
        else:
            with open(self.file_path, 'wb') as fp:
                json.dump(self.artifacts, fp, indent=4)

            # ensure file exists now
            if os.path.exists(self.file_path):
                return True
            return False
