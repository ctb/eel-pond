#! /usr/bin/env python
import screed
import sys
import gzip
import os

prefix='lamp3'

filename = sys.argv[1]

partition_rep = {}
for n, record in enumerate(screed.open(filename)):
    if n % 10000 == 0:
        print '...', n
    partition = record.name.split('.')[-1]
    rep = partition_rep.get(partition, None)
    if not rep or len(rep.sequence) < len(record.sequence):
        partition_rep[partition] = record

new_filename = os.path.basename(filename)
if new_filename.endswith('.gz'):
    new_filename = new_filename[:-3]
if new_filename.endswith('.fasta'):
    new_filename = new_filename[:-6]
new_filename += '.longest.fasta.gz'

print 'creating', new_filename
outfp = gzip.open(new_filename, 'wb')

for p in partition_rep:
    rep = partition_rep[p]
    outfp.write('>%s\n%s\n' % (rep.name, rep.sequence))

print '%d partitions' % (len(partition_rep))
