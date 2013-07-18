#! /usr/bin/env python
import sys
sys.path.insert(0, '/home/t/dev/blastkit/lib')
import blastparser
import cPickle

def collect_best_hits(filename, qfn=None):
    d = {}
    for n, record in enumerate(blastparser.parse_fp(open(filename))):
        if n % 10000 == 0:
            print '...', n
        best_score = None
        for hit in record.hits:
            for match in hit.matches:
                query = record.query_name
                if qfn:
                    query = qfn(query)
                subject = hit.subject_name
                score = match.score

                # only keep the best set of scores for any query
                if best_score and best_score > score:
                    continue
                best_score = score

                x = d.get(query, [])
                x.append((subject, score))
                d[query] = x

            if best_score and best_score != score:
                break
    return d

def parse_ncbi_query(name):
    name = name.split('|')[2:]
    name = '|'.join(name)
    return name

print 'collecting best hits'
d = collect_best_hits(sys.argv[1])

fp = open(sys.argv[2], 'w')
cPickle.dump(d, fp)
