#! /usr/bin/env python
import sys, screed
from cPickle import load
import namedb

ortho = load(open(sys.argv[2]))
homol = load(open(sys.argv[3]))

outfp = open(sys.argv[1] + '.annot', 'w')
for n, record in enumerate(screed.open(sys.argv[1])):
    if n % 10000 == 0:
        print '...', n
    name = record.name
    annot = None

    o = ortho.get(name)
    if o:
        annot = namedb.mouse_names.get(o.split('|')[1])
        annot = "ortho:" + annot
    else:
        h = homol.get(name)
        
        if h:
            h, score = h[0]
            score = round(float(score) / float(len(record.sequence)) * 100)
            annot = namedb.mouse_names[h.split('|')[1]]
            annot = "h=%d%% => " % score + annot
            annot += " "
    if annot:
        annot += " " + record.description
    else:
        annot = record.description

    print >>outfp, ">%s %s\n%s" % (record.name, annot, record.sequence)
