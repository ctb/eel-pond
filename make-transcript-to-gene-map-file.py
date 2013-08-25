#! /usr/bin/env python
import screed, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('transcripts')
    parser.add_argument('tr_to_gene_out')

    args = parser.parse_args()

    tr_to_seq = {}
    for n, record in enumerate(screed.open(args.transcripts)):
        if n % 25000 == 0:
            print '...', n
        tr = record.name.split('.')[2]
        assert tr.startswith('tr')

        x = tr_to_seq.get(tr, [])
        x.append(record.name)
        tr_to_seq[tr] = x

    fp = open(args.tr_to_gene_out, 'w')
    for k in sorted(tr_to_seq):
        for v in tr_to_seq[k]:
            print >>fp, "%s\t%s" % (k, v)
        

if __name__ == '__main__':
    main()
