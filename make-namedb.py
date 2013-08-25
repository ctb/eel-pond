#! /usr/bin/env python
# take an NCBI file and make a dumpd connecting identifier with description.
from cPickle import dump
import screed
import sys

outfile = sys.argv[2]

d = {}
e = {}
for record in screed.open(sys.argv[1]):
    if record.name.startswith('gi|'):
       ident = record.name.split('|')[3]
    else:
       ident = record.name
    d[ident] = record.description
    e[ident] = record.name

fp = open(outfile, 'w')
dump(d, fp)

fp = open(outfile + '.fullname', 'w')
dump(e, fp)
