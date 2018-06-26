#!/usr/bin/env python
##
# omnibus - deadbits.
# accept artifacts from Amazon SQS
##
import boto3

from common import warning

from models import create_artifact


class Import(object):
    def __init__(self, sqs_queue=None, amazon_access_key=None, amazon_secret_key=None):
        self.sqs_queue = sqs_queue
        self.amazon_access_key = amazon_access_key
        self.amazon_secret_key = amazon_access_key
        self.results = []


    def receive(self):
        """ Convert list of artifact names and other metadata into objects and return to application """
        pass

    def read(self):
        """ Read an SQS queue and add all found items as artifacts to be created """
        pass
