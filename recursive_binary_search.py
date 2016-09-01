#!/usr/bin/python

# File Name: recursive_binary_search.py

# From: http://stackoverflow.com/questions/744256/reading-huge-file-in-python
# Posted by: Joe Koberg at Apr 13 '09 at 16:47

# Modified by: Zena Ng
# Date: September 11, 2012

""" IntegerKeyTextFile Class.
    This module uses a recursive binary search algorithm to find the value,
    for a given key.  The file must consist of two columns of integers.
    The first column, the key must be in ascending order.  The second column
    is the value returned.

    # Add these statements to use class

    import recursive_binary_search
    import imp
    imp.reload(recursive_binary_search)

    Usage:
    search = recursive_binary_search.IntegerKeyTextFile(file)
    value = search[key]
"""

import os, stat

class IntegerKeyTextFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.f = open(self.filename, 'r')
        self.getStatinfo()

    def getStatinfo(self):
        self.statinfo = os.stat(self.filename)
        self.size = self.statinfo[stat.ST_SIZE] # in bytes

    def parse(self, line):
        key, value = line.split()
        k = int(key)
        v = int(value)
        return (k,v)

    def __getitem__(self, key):
        return self.findKey(key)

    def findKey(self, keyToFind, startpoint=0, endpoint=None):
        "Recursively search a text file"

        if endpoint is None:
            endpoint = self.size

        currentpoint = (startpoint + endpoint) // 2

        while True:
            self.f.seek(currentpoint)
            if currentpoint <> 0:
                baddata = self.f.readline() # discard partial line

            keyatpoint = self.f.readline()

            if not keyatpoint:
                return 'key not found'

            k,v = self.parse(keyatpoint)

            if k == keyToFind:
                return v

            if endpoint <= startpoint:
                return 'key not found'

            if k > keyToFind:
                return self.findKey(keyToFind, startpoint, currentpoint - 1)
            else:
                return self.findKey(keyToFind, currentpoint + 1, endpoint)
