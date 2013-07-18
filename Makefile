all: lamp3.x.mouse mouse.x.lamp3 petMar_lamp3.fasta_screed \
	mouse.protein.faa_screed mouse.x.lamp3-longest lamp3-longest.x.mouse \
	lamp3-longest.x.mouse.ortho lamp3.x.mouse.ortho

mouse.protein.faa.psq: mouse.protein.faa
	formatdb -i mouse.protein.faa -o T -p T

lamp3.x.mouse: mouse.protein.faa.psq petMar_lamp3.fasta
	blastall -i petMar_lamp3.fasta -d mouse.protein.faa -e 1e-3 -o lamp3.x.mouse -p blastx

mouse.x.lamp3: petMar_lamp3.fasta.nsq
	blastall -i mouse.protein.faa -d petMar_lamp3.fasta -e 1e-3 -o mouse.x.lamp3 -p tblastn

petMar_lamp3.fasta.nsq:
	formatdb -i petMar_lamp3.fasta -o T -p F

petMar_lamp0.fasta.nsq:
	formatdb -i petMar_lamp0.fasta -o T -p F

petMar_lamp3.fasta_screed: petMar_lamp3.fasta
	python -m screed.fadbm petMar_lamp3.fasta

mouse.protein.faa_screed: mouse.protein.faa
	python -m screed.fadbm mouse.protein.faa

mouse.namedb: mouse.protein.faa
	python make-namedb.py mouse.protein.faa mouse.namedb

petMar_lamp3.longest.fasta: petMar_lamp3.fasta
	python extract-longest-sequence-by-partition.py petMar_lamp3.fasta
	gunzip petMar_lamp3.longest.fasta.gz

petMar_lamp3.longest.fasta.nsq: petMar_lamp3.longest.fasta
	formatdb -i petMar_lamp3.longest.fasta -o T -p F

lamp3-longest.x.mouse: mouse.protein.faa.psq petMar_lamp3.longest.fasta
	blastall -i petMar_lamp3.longest.fasta -d mouse.protein.faa -e 1e-3 -o lamp3-longest.x.mouse -p blastx

mouse.x.lamp3-longest: petMar_lamp3.longest.fasta.nsq mouse.protein.faa
	blastall -i mouse.protein.faa -d petMar_lamp3.longest.fasta -e 1e-3 -o mouse.x.lamp3-longest -p tblastn

lamp3-longest.x.mouse.ortho: lamp3-longest.x.mouse mouse.x.lamp3-longest
	python make-reciprocal-best-hits.py lamp3-longest.x.mouse mouse.x.lamp3-longest lamp3-longest.x.mouse.ortho

lamp3.x.mouse.ortho: lamp3.x.mouse mouse.x.lamp3
	python make-reciprocal-best-hits.py lamp3.x.mouse mouse.x.lamp3 lamp3.x.mouse.ortho

lamp3.x.mouse.homol: lamp3.x.mouse
	python make-uni-best-hits.py lamp3.x.mouse lamp3.x.mouse.homol

petMar_lamp3.fasta.annot: petMar_lamp3.fasta lamp3.x.mouse.ortho #lamp3.x.mouse.homol
	python annotate-seqs.py petMar_lamp3.fasta lamp3.x.mouse.ortho lamp3.x.mouse.homol

# Dylan:
# The following targets use BLAST 2.2.28+. We should remedy the incompatibility at some point.
# They also expect the petMar_lamp* databases in data/ to prevent spew from makeblastdb
# In short these are pretty much a disparate set of targets from above.

EVALUE = -evalue 1e-6
DATA_DIR = data
AS_TSV = -outfmt 6

# This is really just for my computer. there's no ./configure script so... oh well.
THREADED = -num_threads 8

BEST_MATCH = python best_match.py
TOTAL_MATCH = python total_match.py

# Note: Make does not support multiple output targets for a single rule
# without resorting to PHONIES, which will rerun every time. Instead we
# just add noop rules for the other two files and pretend the first one
# is representative of all of them.

data/petMar_lamp3.fasta.nhr:
	makeblastdb -in data/petMar_lamp3.fasta -dbtype nucl
data/petMar_lamp3.fasta.nin: data/petMar_lamp3.fasta.nhr
data/petMar_lamp3.fasta.nsq: data/petMar_lamp3.fasta.nhr

data/petMar_lamp0.fasta.nhr:
	makeblastdb -in data/petMar_lamp0.fasta -dbtype nucl
data/petMar_lamp0.fasta.nin: data/petMar_lamp0.fasta.nhr
data/petMar_lamp0.fasta.nsq: data/petMar_lamp0.fasta.nhr


data/p_marinus.no_vlr.cds.fa:
	python lymphilter.py data/p_marinus.cds.fa data/p_marinus.no_vlr.cds.fa

data/genes_of_interest.faa:
	python accession_lookup.py data/genes_of_interest.tsv $@

data/p_marinus.x.lamp3.tsv: data/petMar_lamp3.fasta.nhr
	blastn -db data/petMar_lamp3.fasta -query data/p_marinus.cds.fa $(EVALUE) $(AS_TSV) > $@

data/p_marinus.no_vlr.x.lamp3.tsv: data/petMar_lamp3.fasta.nhr data/p_marinus.no_vlr.cds.fa
	blastn -db data/petMar_lamp3.fasta -query data/p_marinus.no_vlr.cds.fa $(THREADED) $(EVALUE) $(AS_TSV) > $@

data/p_marinus.no_vlr.x.lamp3.best_matches.tsv: data/p_marinus.no_vlr.x.lamp3.tsv
	$(BEST_MATCH) data/p_marinus.no_vlr.x.lamp3.tsv data/p_marinus.no_vlr.cds.fa > $@

data/p_marinus.no_vlr.x.lamp3.total_matches.tsv: data/p_marinus.no_vlr.x.lamp3.tsv
	$(TOTAL_MATCH) data/p_marinus.no_vlr.x.lamp3.tsv data/p_marinus.no_vlr.cds.fa > $@


data/p_marinus.x.lamp0.tsv: data/petMar_lamp0.fasta.nhr
	blastn -db data/petMar_lamp0.fasta -query data/p_marinus.cds.fa $(EVALUE) $(AS_TSV) > $@

data/p_marinus.no_vlr.x.lamp0.tsv: data/petMar_lamp0.fasta.nhr data/p_marinus.no_vlr.cds.fa
	blastn -db data/petMar_lamp0.fasta -query data/p_marinus.no_vlr.cds.fa $(THREADED) $(EVALUE) $(AS_TSV) > $@

data/p_marinus.no_vlr.x.lamp0.best_matches.tsv: data/p_marinus.no_vlr.x.lamp0.tsv
	$(BEST_MATCH) data/p_marinus.no_vlr.x.lamp0.tsv data/p_marinus.no_vlr.cds.fa > $@

data/p_marinus.no_vlr.x.lamp0.total_matches.tsv: data/p_marinus.no_vlr.x.lamp0.tsv
	$(TOTAL_MATCH) data/p_marinus.no_vlr.x.lamp0.tsv data/p_marinus.no_vlr.cds.fa > $@


data/lamp0.x.lamp3.tsv: data/petMar_lamp3.fasta.nhr
	blastn -db data/petMar_lamp0.fasta -query data/petMar_lamp3.fasta $(THREADED) $(EVALUE) $(AS_TSV) > $@

data/lamp0.x.lamp3.best_matches.tsv: data/lamp0.x.lamp3.tsv
	$(BEST_MATCH) data/lamp0.x.lamp3.tsv data/petMar_lamp3.fasta > $@

data/lamp0.x.lamp3.total_matches.tsv: data/lamp0.x.lamp3.tsv
	$(TOTAL_MATCH) data/lamp0.x.lamp3.tsv data/petMar_lamp3.fasta > $@


data/goi.x.lamp3.tsv: data/petMar_lamp3.fasta.nhr data/genes_of_interest.faa
	tblastn -db data/petMar_lamp3.fasta -query data/genes_of_interest.faa $(THREADED) $(EVALUE) $(AS_TSV) > $@

data/goi.x.lamp3.best_matches.tsv: data/goi.x.lamp3.tsv
	$(BEST_MATCH) data/goi.x.lamp3.tsv data/genes_of_interest.faa > $@

data/goi.x.lamp3.total_matches.tsv: data/goi.x.lamp3.tsv
	$(TOTAL_MATCH) data/goi.x.lamp3.tsv data/genes_of_interest.faa > $@
