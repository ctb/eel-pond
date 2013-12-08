#! /usr/bin/env python
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import *
import argparse
import csv
import numpy
import math
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genes_matrix')
    parser.add_argument('sample_spec')
    parser.add_argument('changed_file')

    args = parser.parse_args()

    sample_spec = args.sample_spec
    assert ',' in sample_spec, "sample_spec should look like x,y"
    n1, n2 = sample_spec.split(',')
    n1 = int(n1)
    n2 = int(n2)

    print 'Got sample spec: %d from condition 1, %d from condition 2' % (n1,n2)

    fieldnames = ['']
    for i in range(n1):
        fieldnames.append('s1.%d' % i)
    for i in range(n2):
        fieldnames.append('s2.%d' % i)

    print 'Loading differentially expressed gene names from', args.changed_file

    changed_names = set()
    fp = open(args.changed_file, 'rb')
    r = csv.DictReader(fp)
    for row in r:
        name = row['transcript family']
        changed_names.add(name)
    fp.close()

    print 'Loading gene matrix from', args.genes_matrix

    changed_values = []
    rows = []
    fp = open(args.genes_matrix, 'rb')
    r = csv.DictReader(fp, delimiter='\t', fieldnames=fieldnames)
    r.next()

    for row in r:
        s1 = 0.0
        for i in range(n1):
            k = 's1.%d' % i
            s1 += float(row[k])
        s1 /= float(n1)

        s2 = 0.0
        for i in range(n2):
            k = 's2.%d' % i
            s2 += float(row[k])
        s2 /= float(n2)

        rows.append((s1, s2))

        if row[''] in changed_names:
            changed_values.append((s1, s2))

    rows = numpy.array(rows)
    changed_values = numpy.array(changed_values)

    print 'plotting...'

    plot(rows[:,0], rows[:,1], 'bo', alpha='0.1', label='all genes')
    plot(changed_values[:,0], changed_values[:,1], 'r.', alpha='0.2', label='DE genes')

    ax = axes()
    ax.set_yscale('log')
    ax.set_xscale('log')
    legend(loc='upper left')
    xlabel('Expression in condition 1')
    ylabel('Expression in condition 2')

    filename = os.path.basename(args.genes_matrix) + '.png'
    print 'Output figure to:', filename
    savefig(filename)

if __name__ == '__main__':
    main()
