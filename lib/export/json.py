#!/usr/bin/env python
##
# omnibus - deadbits.
# export artifacts to a local JSON file
##
import os
import json

from common import success
from common import warning


class Export(object):
    def __init__(self, artifacts=None, file_path=None):
        self.artifacts = artifacts
        self.file_path = file_path


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
                success('Artifacts successfully exported to JSON file (%s)' % self.file_path)
