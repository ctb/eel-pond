#! /usr/bin/env python
import sys, screed
from cPickle import load
import namedb
import argparse
import os.path

def transform_name(name, is_ncbi):
    if not is_ncbi:
        return name

    return name.split('|')[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('transcripts')
    parser.add_argument('ortho')
    parser.add_argument('homol')
    parser.add_argument('-z', '--no-ncbi', action='store_false',
                        dest='ncbi', default='True')
    args = parser.parse_args()

    transcript_file = args.transcripts
    ortho = load(open(args.ortho))
    homol = load(open(args.homol))

    tr_dict = {}
    print 'Scanning sequences -- first pass to gather info'
    for n, record in enumerate(screed.open(transcript_file)):
        tr = record.name.split('.')[2]
        assert tr.startswith('tr')

        if n % 25000 == 0:
            print '...', n
        name = record.name
        annot = None

        o = ortho.get(name)
        if o:
            annot = namedb.mouse_names.get(transform_name(o, args.ncbi))
            tr_dict[tr] = ('ortho', annot)
        else:
            if tr in tr_dict and tr_dict[tr][0] == 'ortho':
                continue

            h = homol.get(name)

            if h:
                oldscore = 0.
                if tr in tr_dict:
                    oldscore, _ = tr_dict[tr]

                h, score = h[0]
                score = round(float(score) / float(len(record.sequence)) * 100)
                annot = namedb.mouse_names[transform_name(h, args.ncbi)]

                if score > oldscore:
                    tr_dict[tr] = (oldscore, annot)

    outfilename = os.path.basename(transcript_file) + '.annot'
    outfp = open(outfilename, 'w')


    annot_ortho_count = 0
    annot_homol_count = 0
    annot_tr_count = 0

    print 'second pass: annotating'
    for n, record in enumerate(screed.open(transcript_file)):
        tr = record.name.split('.')[2]

        if n % 25000 == 0:
            print '... x2', n
        name = record.name
        annot = None

        o = ortho.get(name)
        if o:
            annot = namedb.mouse_names.get(transform_name(o, args.ncbi))
            annot = "ortho:" + annot
            annot_ortho_count += 1
        else:
            h = homol.get(name)

            if h:
                h, score = h[0]
                score = round(float(score) / float(len(record.sequence)) * 100)
                annot = namedb.mouse_names[transform_name(h, args.ncbi)]
                annot = "h=%d%% => " % score + annot
                annot += " "
                annot_homol_count += 1
            else:
                if tr in tr_dict:
                    score, annot = tr_dict[tr]
                    if score == 'ortho':
                        annot = 'transcript family ortho to:' + annot
                    else:
                        annot = 'transcript family homol to:' + annot
                    annot_tr_count += 1

        if annot:
            annot += " " + record.description
        else:
            annot = record.description

        print >>outfp, ">%s %s\n%s" % (record.name, annot, record.sequence)

    print '----'
    print '%d sequences total' % n
    print '%d annotated / ortho' % annot_ortho_count
    print '%d annotated / homol' % annot_homol_count
    print '%d annotated / tr' % annot_tr_count
    print '%d total annotated' % (annot_ortho_count + annot_homol_count + annot_tr_count)
    print ''
    print 'annotated sequences in:', outfilename

if __name__ == '__main__':
    main()
