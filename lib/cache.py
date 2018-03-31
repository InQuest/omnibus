from __future__ import absolute_import

from .abc import DefaultMapping


class _DefaultSize(object):
    def __getitem__(self, _):
        return 1

    def __setitem__(self, _, value):
        assert value == 1

    def pop(self, _):
        return 1


class Cache(DefaultMapping):
    __size = _DefaultSize()


    def __init__(self, maxsize, missing=None, getsizeof=None):
        if missing:
            self.__missing = missing
        if getsizeof:
            self.__getsizeof = getsizeof
            self.__size = dict()
        self.data = dict()
        self.__currsize = 0
        self.__maxsize = maxsize


    def __repr__(self):
        """Return name, iems, maxsize and current size"""
        return '%s(%r, maxsize=%r, currsize=%r)' % (
            self.__class__.__name__,
            list(self.data.items()),
            self.__maxsize,
            self.__currsize,
        )


    def __getitem__(self, key):
        """Get item by key"""
        try:
            return self.data[key]
        except KeyError:
            return self.__missing__(key)


    def __setitem__(self, key, value):
        """Set item by key and value"""
        maxsize = self.__maxsize
        size = self.getsizeof(value)
        if size > maxsize:
            raise ValueError('value too large')
        if key not in self.data or self.__size[key] < size:
            while self.__currsize + size > maxsize:
                self.popitem()
        if key in self.data:
            diffsize = size - self.__size[key]
        else:
            diffsize = size
        self.data[key] = value
        self.__size[key] = size
        self.__currsize += diffsize


    def __delitem__(self, key):
        """Remove item by key"""
        size = self.__size.pop(key)
        del self.data[key]
        self.__currsize -= size


    def __contains__(self, key):
        """Check if cache contains item by key"""
        return key in self.data


    def __missing__(self, key):
        """Add item by key if missing"""
        value = self.__missing(key)
        try:
            self.__setitem__(key, value)
        except ValueError:
            pass  # value too large
        return value


    def __iter__(self):
        """Iterate over items"""
        return iter(self.data)


    @property
    def __len__(self):
        """Get number of items"""
        return len(self.data)


    @staticmethod
    def __getsizeof(value):
        return 1


    @staticmethod
    def __missing(key):
        raise KeyError(key)


    @property
    def maxsize(self):
        """The maximum size of the cache."""
        return self.__maxsize

    @property
    def currsize(self):
        """The current size of the cache."""
        return self.__currsize


    def getsizeof(self, value):
        """Return the size of a cache element's value."""
        return self.__getsizeof(value)
