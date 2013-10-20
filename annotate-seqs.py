#! /usr/bin/env python
import sys, screed
from cPickle import load
import namedb
import argparse
import os.path
import csv

def transform_name(name):
    if namedb.is_ncbi:
        return name.split('|')[1]
    return name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('transcripts')
    parser.add_argument('ortho')
    parser.add_argument('homol')
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
            annot = namedb.mouse_names.get(transform_name(o))
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
                annot = namedb.mouse_names[transform_name(h)]

                if score > oldscore:
                    tr_dict[tr] = (oldscore, annot)

    outfilename = os.path.basename(transcript_file) + '.annot'
    outfp = open(outfilename, 'w')

    csvfile = os.path.basename(transcript_file) + '.annot.csv'
    csvfp = open(csvfile, 'w')
    csv_writer = csv.writer(csvfp)

    csvfile2 = os.path.basename(transcript_file) + '.annot.large.csv'
    csvfp2 = open(csvfile2, 'w')
    csv_large = csv.writer(csvfp2)

    csv_writer.writerow(["sequence name", "unique ID", "Transcript family",
                         "ortholog", "homology score", "homolog",
                         "family orthology", "family homology",
                         "additional information"])
    csv_large.writerow(["sequence name", "unique ID", "Transcript family",
                         "ortholog", "homology score", "homolog",
                         "family orthology", "family homology",
                         "additional information", "sequence"])

    annot_ortho_count = 0
    annot_homol_count = 0
    annot_tr_count = 0

    print 'second pass: annotating'
    for n, record in enumerate(screed.open(transcript_file)):
        seqid = record.name.split('.')[1]
        tr = record.name.split('.')[2]

        ortho_col = ""
        homol_score = ""
        homol_col = ""
        family_ortho_col = ""
        family_homol_col = ""

        if n % 25000 == 0:
            print '... x2', n
        name = record.name
        annot = None

        o = ortho.get(name)
        if o:
            annot = namedb.mouse_names.get(transform_name(o))
            ortho_col = annot
            annot = "ortho:" + annot
            annot_ortho_count += 1
        else:
            h = homol.get(name)

            if h:
                h, score = h[0]
                score = round(float(score) / float(len(record.sequence)) * 100)
                annot = namedb.mouse_names[transform_name(h)]

                homol_score = "%d" % score
                homol_col = annot

                annot = "h=%d%% => " % score + annot
                annot += " "

                annot_homol_count += 1
            else:
                if tr in tr_dict:
                    score, annot = tr_dict[tr]
                    if score == 'ortho':
                        family_ortho_col = annot
                        annot = 'transcript family ortho to:' + annot
                    else:
                        family_homol_col = annot
                        annot = 'transcript family homol to:' + annot
                    annot_tr_count += 1

        if annot:
            annot += " " + record.description
        else:
            annot = record.description

        print >>outfp, ">%s %s\n%s" % (record.name, annot, record.sequence)
        csv_writer.writerow([record.name, seqid, tr,
                             ortho_col,
                             homol_score,
                             homol_col,
                             family_ortho_col,
                             family_homol_col,
                             record.description])
        csv_large.writerow([record.name, seqid, tr,
                             ortho_col,
                             homol_score,
                             homol_col,
                             family_ortho_col,
                             family_homol_col,
                             record.description,
                             record.sequence])

    print '----'
    print '%d sequences total' % n
    print '%d annotated / ortho' % annot_ortho_count
    print '%d annotated / homol' % annot_homol_count
    print '%d annotated / tr' % annot_tr_count
    print '%d total annotated' % (annot_ortho_count + annot_homol_count + annot_tr_count)
    print ''
    print 'annotated sequences in FASTA format:', outfilename
    print 'annotation spreadsheet in:', csvfile
    print 'annotation spreadsheet with sequences (warning: LARGE):', csvfile2

if __name__ == '__main__':
    main()
