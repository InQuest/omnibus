#!/usr/bin/env python
##
# omnibus - deadbits.
#
# in-memory queue for keeping a list of recently active
# artifacts to be interacted with inside an omnibus session.
##

from redis import Redis

from common import error

from common import utf_decode
from common import utf_encode


class RedisCache(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6379
        self.database = 1

        self.ttl = 9999999999999
        if self.ttl is not None:
            self.ttl = int(self.ttl)

        try:
            self.db = Redis(db=self.database, host=self.host,
                port=self.port, socket_timeout=None)
        except:
            self.db = None


    def send(self, message, queue_name):
        """ Send a new message to a specific Redis queue """
        message = utf_encode(message)
        try:
            self.db.lpush(queue_name, message)
        except Exception as err:
            error('[redis] failed to push message to queue %s (error: %s)' % (queue_name, str(err)))
            pass


    def receive(self, queue_name):
        """ Return most recent message from a given Redis queue"""
        try:
            ret_val = self.db.lindex(queue_name, -1)
            if isinstance(ret_val, bytes):
                return utf_decode(ret_val)
            return ret_val
        except Exception as err:
            error('[redis] failed to receive message from queue %s (error: %s)' % (queue_name, str(err)))
            pass


    def delete(self, names):
        """ Remove one or more keys by name """
        try:
            self.db.delete(names)
        except Exception as err:
            error('[redis] failed to delete artifacts (error: %s)' % str(err))


    def exists(self, key):
        """ Check if value exists by key """
        return self.db.exists(key)


    def get(self, key):
        """ Get a value from redis by key """
        retval = self.db.get(key)
        if isinstance(retval, bytes):
            return utf_decode(retval)
        return retval


    def set(self, key, value, ttl=None):
        """ Set a value in cache with optional TTL """
        if ttl is None:
            ttl = self.ttl
        if isinstance(value, str):
            value = utf_encode(value)
        # backward compatibility (Redis v2.2)
        self.db.setnx(key, value)
        self.db.expire(key, ttl)


    def acknowledge(self, queue_name):
        try:
            return self.db.rpop(queue_name)
        except Exception as err:
            error('[redis] failed to acknowledge queue %s (error: %s)' % (queue_name, str(err)))
            pass


    def count_queued(self, *queues):
        """ Get count of all messages in all queues"""
        queue_dict = {}
        for queue in queues:
            try:
                queue_dict[queue] = self.db.llen(queue)
            except Exception as err:
                error('[redis] failed to count queued messages (queues: %s) (error: %s)' % (str(queue)), str(err))
                pass
        return queue_dict


    def event_stream(self, queue_name):
        """ Use pubsub method to listen for messages from a specific subscription/queue """
        pub_sub = self.db.pubsub()
        pub_sub.subscribe(queue_name)
        for message in pub_sub.listen():
            if isinstance(message, bytes):
                yield utf_decode(message['data'])
            else:
                yield message['data']


    def clear_queue(self, queue_name):
        """ Clear a queue by deleting the key """
        try:
            return self.db.delete(queue_name)
        except Exception as err:
            error('[redis] failed to delete queue %s (error: %s)' % (queue_name, str(err)))
            pass


    def flush(self):
        """ Flush opened database entirely """
        self.db.flushdb()
