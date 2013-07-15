#!/usr/bin/env python
#
# argv[1]: blastn tsv output
# argv[2]: query fasta file

import sys
import re
import itertools
from Bio import SeqIO

vlr_re = re.compile(((len(sys.argv) > 3) and sys.argv[3]) or r'lymphocyte')

with open(sys.argv[1], 'rU') as in_handle, open(sys.argv[2], 'w') as out_handle:
        sequences = SeqIO.parse(in_handle, 'fasta')

        def lymphilter(sequences):
            for record in sequences:
                if not vlr_re.search(record.description):
                    yield record

        SeqIO.write(lymphilter(sequences), out_handle, 'fasta')

