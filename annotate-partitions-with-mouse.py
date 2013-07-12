#! /usr/bin/env python
import sys
sys.path.insert(0, '/home/t/dev/blastkit/lib')
import blastparser

import namedb

BITSCORE_CUTOFF=100

def collect_blast_hits_by_family(blastfile):
    d = {}
    for record in blastparser.parse_fp(open(blastfile)):
        tr = record.query_name.split('.')[2]
        assert tr.startswith('tr')
        tr = int(tr[2:])

        collect = []
        for hit in record.hits:
            for match in hit.matches:
                if match.score >= BITSCORE_CUTOFF:
                    name = hit.subject_name.split('|')[1]
                    collect.append((name, match.score))

        x = d.get(tr, [])
        x.append(collect)
        d[tr] = x

    return d

hits_by_family = collect_blast_hits_by_family(sys.argv[1])

for tr in hits_by_family:
    hitlist = hits_by_family[tr]
    all_hits = []
    for h in hitlist:
        all_hits.extend(h)

    all_hits = sorted(all_hits, key=lambda x:x[1], reverse=True)
    gene_idents = map(lambda x:x[0], all_hits)
    gene_names = map(lambda x: namedb.mouse_names[x], gene_idents)
    print tr, set(gene_names[:2])
    
