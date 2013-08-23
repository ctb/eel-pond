#! /usr/bin/env python
import sys
import blastparser
import cPickle
import argparse

def collect_best_hits(filename, qfn=None):
    d = {}
    for n, record in enumerate(blastparser.parse_fp(open(filename))):
        if n % 25000 == 0:
            print '...', filename, n
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tr_vs_ref')
    parser.add_argument('ref_vs_tr')
    parser.add_argument('output')
    parser.add_argument('-z', '--no-ncbi', action='store_false',
                        dest='ncbi', default='True')
    args = parser.parse_args()

    tr_vs_ref = args.tr_vs_ref
    ref_vs_tr = args.ref_vs_tr
    outputfilename = args.output
    
    if 1:
        print 'collecting best hits from:', tr_vs_ref
        d = collect_best_hits(tr_vs_ref)

        print 'collecting best hits from:', ref_vs_tr
        if args.ncbi:
            e = collect_best_hits(ref_vs_tr, parse_ncbi_query)
        else:
            e = collect_best_hits(ref_vs_tr)

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

    fp = open(outputfilename, 'w')
    cPickle.dump(dd, fp)
    cPickle.dump(ee, fp)

if __name__ == '__main__':
    main()
