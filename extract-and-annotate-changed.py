#! /usr/bin/env python
import screed
import argparse
import csv

P=0.05

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('changed_file')
    parser.add_argument('transcript_file')
    parser.add_argument('output')

    args = parser.parse_args()

    print 'Loading changed list from:', args.changed_file
    tr_dict = {}
    fp = open(args.changed_file, 'rb')
    r = csv.DictReader(fp, delimiter='\t',
                 fieldnames=['tr', 'p_equal', 'p_diff', 'postfc', 'realfc'])
    r.next()

    for row in r:
        tr = row['tr']
        tr_dict[tr] = row

    print 'Loading transcript matrix from:', args.transcript_file
    annots = {}
    for record in screed.open(args.transcript_file):
        tr = record.name.split('.')[2]
        assert tr.startswith('tr')

        # find the location of the x_of_y string; before that is the
        # annotation.
        annot_loc = record.description.find('_of_')
        assert annot_loc > 0
        while annot_loc > 0 and record.description[annot_loc] != ' ':
            annot_loc -= 1
        assert annot_loc >= 0, annot_loc

        # if we got anything, record it.
        if annot_loc > 0:
            annot = record.description[:annot_loc].strip()

            # eliminate 'transcript family' annotations since the
            # original annotations will be gathered.
            if annot.startswith('transcript family'):
                continue

            x = annots.get(tr, [])
            x.append(annot)
            annots[tr] = x

    def sort_by_ortho(a, b):
        if a.startswith('ortho'):
            return -1
        return 0

    for n, k in enumerate(annots):
        annot = sorted(set(annots[k]), cmp=sort_by_ortho)
        annots[k] = "; ".join(annot)

    ###

    diff_tr = []
    for tr in tr_dict:
        row = tr_dict[tr]
        p_equal = float(row['p_equal'])
        if p_equal > P:         # ignore!
            continue

        postfc = float(row['postfc'])
        realfc = float(row['realfc'])

        diff_tr.append((p_equal, postfc, realfc, tr))

    diff_tr.sort()

    ###

    print '%d of %d total genes diff expressed at P > %f' % (len(diff_tr),
                                                             len(tr_dict),
                                                             1-P)

    print 'Writing differentially expressed genes list to', args.output
    outfp = open(args.output, 'w')
    w = csv.writer(outfp)

    w.writerow(['p diff expr', 'PostFC', 'RealFC', 'transcript family', 'annotation'])
    for p_equal, postfc, realfc, tr in diff_tr:
        w.writerow([1.0-p_equal, postfc, realfc, tr, annots.get(tr, '')])
    outfp.close()

if __name__ == '__main__':
    main()
