#!/usr/bin/env python
#
# argv[1]: blastn tsv output
# argv[2]: query fasta file

import sys
import csv
from bitarray import bitarray
from Bio import SeqIO

seen_queries = dict()

handle = open(sys.argv[2], 'r')
queries = SeqIO.to_dict(SeqIO.parse(handle, 'fasta'))
handle.close()

with open(sys.argv[1]) as in_file:
    reader = csv.reader(in_file, delimiter='\t')
    for row in reader:
        e_value = float(row[10])

        if e_value > 1e-20:
            continue

        query, length, q_start, q_end = (row[0], int(row[3]), int(row[6]), int(row[7]))

        assert(q_start < q_end)

        if not query in seen_queries:
            seen_queries[query] = bitarray('0') * len(queries[query].seq)

        seen_queries[query][q_start:q_end] = bitarray('1') * (q_end - q_start + 1)

print 'query\tmatched letters\ttotal letters\tpercent matched letters'
for k, mask in seen_queries.iteritems():
    print '%s\t%i\t%i\t%f' % (k, mask.count(), len(mask), float(mask.count())/len(mask))
