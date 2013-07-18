#!/usr/bin/env python
#
# argv[1]: genes of interest (tsv with 'accession' column)

import csv
import sys
from Bio import Entrez, SeqIO

Entrez.email = 'lukes.dylan@gmail.com'

with open(sys.argv[1], 'rU') as in_file, open(sys.argv[2], 'w') as out_file:
    goi = csv.DictReader(in_file, delimiter='\t')

    accessions = []

    for (accession, row) in ((row['accession'], row) for row in goi):
        if accession == 'N/A':
            print 'Skipping `%s\'  -  No applicable accession number.' % (row['symbol'])
            continue
        else:
            accessions.append(accession + '[accn]')

    assert(len(accessions) < 100000)  # would require paging

    print '\nSearching by accession in `protein` database...'

    search_opts = {
        'db': 'protein',
        'term': ' OR '.join(accessions),
        'usehistory': 'y'
    }

    search = Entrez.esearch(**search_opts)
    print 'Parsing search results...'
    result = Entrez.read(search)
    search.close()

    print 'Done!'
    print '\nFetching FASTA records...'

    fetch_opts = {
        'db': 'protein',
        'query_key': result['QueryKey'],
        'webenv': result['WebEnv'],
        'retmode': 'text',
        'rettype': 'fasta'
    }

    fetch = Entrez.efetch(**fetch_opts)
    out_file.write(fetch.read())
    fetch.close()

    print 'Done!\nFASTA records saved to %s' % (sys.argv[2])
