#!/usr/bin/env python
# process nodes.dmp file and output list of vertebrate taxids from it

import sys

nodes = sys.argv[1]
vertID = 7742
idmap = {} # maps ID to parent ID

fhn = open(nodes, 'rb')
for line in fhn:
    fld = line.split("\t|\t")
    #print "'"+fld[0]+"'" + " parent: '" + fld[1] + "'"
    idmap[ int(fld[0]) ] = int( fld[1] )
fhn.close()

# map created, make a copy of it in a list for safety
idlist = []
for key, value in idmap.iteritems():
    idlist.append(key)

for id in idlist:
    parent = idmap[id]
    while parent != vertID and parent > 1:
        parent = idmap[parent]
    if parent == vertID:
        print id, parent
