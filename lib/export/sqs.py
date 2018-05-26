#!/usr/bin/env python
##
# omnibus - deadbits.
# export artifacts to Amazon SQS queue
##
import boto3

from common import warning


class Export(object):
    def __init__(self, artifacts=None, sqs_queue=None, amazon_access_key=None, amazon_secret_key=None):
        self.sqs_queue = sqs_queue
        self.artifacts = artifacts
        self.amazon_access_key = amazon_access_key
        self.amazon_secret_key = amazon_access_key
        self.results = []


    def send(self):
        """ Send all artifacts to the provided Amazon SQS queue """
        pass
