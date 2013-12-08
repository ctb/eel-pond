#! /usr/bin/env python
import csv
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genes_matrix')
    parser.add_argument('-f', '--force', dest='force', action='store_true')

    args = parser.parse_args()

    print 'Loading matrix from:', args.genes_matrix

    rows = []
    fp = open(args.genes_matrix, 'rb')
    r = csv.DictReader(fp, delimiter='\t')
    for row in r:
        rows.append(row)

    print 'done loading; now opening output files'

    file_d = {}
    for orig_filename in row.keys():
        if not orig_filename:
            continue
        filename = os.path.basename(orig_filename)
        if not args.force:
            assert not os.path.exists(filename), '%s should not exist' % filename
        fp = open(filename, 'wb')
        w = csv.writer(fp, delimiter='\t')
        file_d[orig_filename] = w

        w.writerow(['gene_id', 'transcript_id(s)', 'length',
                    'effective_length', 'expected_count',
                    'TPM', 'FPKM'])

    print 'dumping to %d output files' % len(file_d)

    for row in rows:
        tr = row['']
        for k in row:
            if not k:
                continue
            w = file_d[k]
            w.writerow([tr, '', 0, 0, "%.2f" % float(row[k]), 0, 0])

if __name__ == '__main__':
    main()
