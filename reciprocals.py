#!/usr/bin/env python

import re
import sys
import argparse
import cPickle
from pprint import pprint
from Bio.Blast import NCBIStandalone

ident = lambda _: _

def best_hsp(alignment):
    return max(alignment.hsps, key=lambda h: h.score)


def best_alignment(record):
    if not record.alignments:
        return None
    return max(record.alignments, key=lambda a: best_hsp(a).score)


def gen_lookup(records, key_fn=ident):
    d = {}
    for record in records:
        best = best_alignment(record)
        if not best:
            continue
        assert(not key_fn(record.query) in d)  # no duplicates please :)
        d[key_fn(record.query)] = best
    return d


def gen_reciprocal_map(g1, g2, kfn1=ident, kfn2=ident):
    for k1, v1 in g1:
        for k2, v2 in g2:
            if k1 == kfn1(v2.title) and k2 == kfn2(v1.title):
                yield (k1, k2)


argparser = argparse.ArgumentParser(description='Find reciprocal best hits in two BLAST outputs')
argparser.add_argument('blast1', type=file, help='BLAST results')
argparser.add_argument('blast2', type=file, help='inverted BLAST results')
argparser.add_argument('-d', '--dump', type=argparse.FileType('w'),
                       dest='dump_file',
                       help='pickle intermediate results in tempfile')
argparser.add_argument('-l', '--load', type=argparse.FileType('r'),
                       dest='load_file',
                       help='depickle intermediate results from tempfile')
argparser.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout)

args = argparser.parse_args()
assert not (args.load_file and args.dump_file)

parser1 = NCBIStandalone.BlastParser()
parser2 = NCBIStandalone.BlastParser()

# PXL: PMZ(Q) x Lamp3(S), LXP: Lamp3(Q) x PMZ(S)
pxl_records = NCBIStandalone.Iterator(args.blast1, parser1)
lxp_records = NCBIStandalone.Iterator(args.blast2, parser2)

pxl_re = re.compile(r'(PMZ_[^\s]+)')
pxl_key_fn = lambda k: pxl_re.findall(k)[0]
lxp_re = re.compile(r'(lamp3[^\s]+ [^\s]+ len\d+)')  # matching 'not whitespace' is faster and more robust
lxp_key_fn = lambda k: lxp_re.findall(k)[0]

pxl_lookup, lxp_lookup = None, None

if args.load_file:
    pxl_lookup = cPickle.load(args.load_file)
    lxp_lookup = cPickle.load(args.load_file)
else:
    pxl_lookup = make_lookup(pxl_records, pxl_key_fn)
    lxp_lookup = make_lookup(lxp_records, lxp_key_fn)

    if args.dump_file:
        cPickle.dump(pxl_lookup, args.dump_file)
        cPickle.dump(lxp_lookup, args.dump_file)

assert pxl_lookup and lxp_lookup


for k, v in gen_reciprocal_map(pxl_lookup, lxp_lookup, pxl_key_fn, lxp_key_fn):
    args.outfile.write('%s\t%s\n' % (k, v))
