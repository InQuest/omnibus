#!/usr/bin/env python
##
# omnibus - deadbits
# accept artifacts from a local text file
##

from common import is_valid
from common import warning

from models import create_artifact


class Import(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read()
        self.artifacts = []


    def receive(self):
        """ convert list of artifact names into objects and return to application """
        try:
            for item in self.data:
                self.artifacts.append(create_artifact(artifact_name=item, source='local list'))
        except:
            warning('Could not extract any valid artifacts from %s' % self.file_path)


    def read(self):
        """ Read a file with one artifact name per line and return all entries """
        if is_valid(self.file_path):
            data = (open(self.file_path, 'rb').read()).split('\n')
            return data
        return None
