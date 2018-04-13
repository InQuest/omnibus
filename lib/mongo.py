#!/usr/bin/env python
##
# omnibus - deadbits.
# mongodb interaction
##

import pymongo

from common import error

from common import get_option


class Mongo(object):
    def __init__(self, config):
        self._host = get_option('mongo', 'host', config)
        self._port = int(get_option('mongo', 'port', config))
        self._server = '%s:%s' % (self._host, self._port)
        try:
            self.conn = pymongo.MongoClient(self._server)
        except Exception as err:
            error('failed to connect to Mongo instance: %s' % str(err))
            raise err

        self.db = self.conn['omnibus']


    def use_coll(self, collection):
        return self.db[collection]


    def get_value(self, collection, query, key):
        """ get value of given key from db query """
        coll = self.use_coll(collection)
        result = dict(coll.find_one(query, {key: 1}))
        if result == {}:
            return None
        return result[key]


    def exists(self, collection, query):
        coll = self.use_coll(collection)
        result = coll.find_one(query)
        if result is None:
            return False
        return True


    def count(self, collection, query={}):
        coll = self.use_coll(collection)
        return coll.count(query)


    def insert_one(self, collection, data):
        if isinstance(data, object):
            data = data.__dict__

        coll = self.use_coll(collection)
        doc_id = None

        try:
            doc_id = coll.insert(data)
        except Exception as err:
            error('failed to index data: %s' % str(err))
            pass

        return str(doc_id)


    def update_one(self, collection, query, new_data):
        coll = self.use_coll(collection)
        doc_id = None

        try:
            doc_id = coll.update(query, {'$set': new_data})
        except:
            error('failed to update documents: %s' % query)
            pass

        return doc_id


    def delete_one(self, collection, query):
        coll = self.use_coll(collection)
        try:
            coll.remove(query)
        except:
            error('failed to delete documets: %s' % query)
            pass


    def find_recent(self, collection, query={}, num_items=25, offset=0):
        coll = self.use_coll(collection)
        total = self.count(collection, query)
        result = []

        if total < num_items:
            result = list(coll.find(query))

        elif offset <= 0:
            result = list(coll.find(query).limit(num_items).sort([('_id', -1)]))

        else:
            result = list(coll.find(query).skip(offset).limit(num_items).sort([('_id', -1)]))

        return result


    def find(self, collection, query, one=False):
        """ return multiple query results as dict or single result as list """
        coll = self.use_coll(collection)

        if one:
            result = coll.find_one(query)

            if result is not None:
                d = dict(result)
                del d['_id']
                return d

            return {}

        else:
            result = coll.find(query)

            if result is not None:
                l = list(result)
                for i in l:
                    del i['_id']
                return l

            return []
