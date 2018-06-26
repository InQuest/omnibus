#!/usr/bin/env python
##
# omnibus - deadbits
# import artifacts from CSIRTG
##
from common.http import get

from common import error
from common import running
from common import success
from common import warning
from common import get_apikey
from common import detect_type

from models import create_artifact
from models import artifact_types


class Import(object):
    def __init__(self, feed=None, user=None, limit=50):
        """Import artifacts from a users CSIRTG feed"""
        self.feed = feed
        self.user = user
        self.limit = limit
        self.api_key = get_apikey('csirtg')
        self.headers = {
            'Authorization': 'Token token=%s' % self.api_key,
            'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)',
            'Accept': 'application/vnd.csirtg.v1'
        }

        if self.limit is not None:
            self.feed_url = 'https://csirtg.io/api/users/%s/feeds/%s?limit=%d' % (self.user, self.feed, self.limit)
        else:
            self.feed_url = 'https://csirtg.io/api/users/%s/feeds/%s' % (self.user, self.feed)


    def receive(self):
        artifacts = []

        status, response = get(self.feed_url, headers=self.headers)
        if status:
            jdata = response.json()

            if len(jdata['indicators']) > 0:

                for ioc in jdata['indicators']:
                    artifact_type = detect_type(ioc['indicator'])
                    if artifact_type not in artifact_types:
                        warning('Discovered artifact from CSRIRTG not accepted by Omnibus')
                        pass
                    else:
                        artifact = {
                            'name': ioc['indicator'],
                            'source': 'csirtg - %s %s' % (self.user, self.feed),
                            'type': artifact_type
                        }
                        artifacts.append(artifact)

            if len(artifacts) > 0:
                success('Found %d artifacts for import' % len(artifacts))
                # send Artifacts to Omnibus for creation
                self.send(artifacts)
            else:
                error('No valid artifacts found for import')


    def send(self, artifacts):
        """ Create artifacts in MongoDB """
        running('Attempting to add new artifacts to database ...')
        for ioc in artifacts:
            artifact = create_artifact(name=ioc['name'], type=ioc['type'], source=ioc['source'])

            if not self.db.exists(artifact.type, {'name': artifact.name}):
                doc_id = self.db.insert_one(artifact.type, artifact)
                if doc_id is not None:
                    success('Created new artifact (%s - %s)' % (artifact.name, artifact.type))

            else:
                warning('Skipping duplicated artifact (%s)' % artifact.name)
