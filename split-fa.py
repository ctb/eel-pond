#! /usr/bin/env python
import sys
import screed

N = 1

for n, record in enumerate(screed.open(sys.argv[1])):
    if n % 100000 == 0:
        fp = open(sys.argv[1] + '.%d' % N, 'w')
        N += 1

    print >>fp, ">%s\n%s\n" % (record.name, record.sequence)
