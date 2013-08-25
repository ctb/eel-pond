#! /usr/bin/env python
import screed
import sys
import gzip
import os

prefix=sys.argv[1]

filename = sys.argv[2]

# first pass: count partition sizes
partition_sizes = {}
for n, record in enumerate(screed.open(filename, parse_description=0)):
    if n % 10000 == 0:
        print '...', n
    partition = record.name.split()[-1]
    partition_sizes[partition] = partition_sizes.get(partition, 0) + 1

# show top 10 biggest partitions
for n, (_, size) in enumerate(sorted(partition_sizes.items(),
                                     key=lambda x: -x[1])):
    print n, size
    if n == 50:
        break

# now, make a sensible header for each sequence that uniquely ids it
partition_sofar = {}
seq_id = 1

new_filename = os.path.basename(filename)
if new_filename.endswith('.gz'):
    new_filename = new_filename[:-3]
if new_filename.endswith('.fasta'):
    new_filename = new_filename[:-6]
new_filename += '.renamed.fasta.gz'

print 'creating', new_filename
outfp = gzip.open(new_filename, 'wb')

for n, record in enumerate(screed.open(sys.argv[2], parse_description=0)):
    if n % 10000 == 0:
        print '...writing', n
    partition = record.name.split()[-1]
    sofar = partition_sofar.get(partition, 0) + 1
    partition_sofar[partition] = sofar
    partition_size = partition_sizes[partition]

    new_name = '%s.id%d.tr%s %d_of_%d_in_tr%s len=%d id=%s tr=%s' % \
        (prefix, seq_id, partition, sofar, partition_size, partition, len(record.sequence), seq_id, partition)
    outfp.write('>%s\n%s\n' % (new_name, record.sequence))
    seq_id += 1
