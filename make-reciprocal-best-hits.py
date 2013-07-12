#! /usr/bin/env python
import sys
sys.path.insert(0, '/home/t/dev/blastkit/lib')
import blastparser
import cPickle

def collect_best_hits(filename, qfn=None):
    d = {}
    for record in blastparser.parse_fp(open(filename)):
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

if 1:
    d = collect_best_hits(sys.argv[1])
    e = collect_best_hits(sys.argv[2], parse_ncbi_query)

    fp = open('xxx', 'w')
    cPickle.dump(d, fp)
    cPickle.dump(e, fp)
else:
    assert 0
    fp = open('xxx')
    d = cPickle.load(fp)
    e = cPickle.load(fp)

dd = {}
ee = {}

for k in d:
    v = map(lambda x: x[0], d[k])
    
    for k2 in v:
        v2 = map(lambda x: x[0], e.get(k2, []))

        if k in v2:
            dd[k] = k2
            ee[k2] = k

fp = open(sys.argv[3], 'w')
cPickle.dump(dd, fp)
cPickle.dump(ee, fp)
