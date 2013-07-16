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
	python -m screed.fadbm patMar_lamp3.fasta

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



# Dylan:
# The following targets use BLAST 2.2.28+. We should remedy the incompatibility at some point.
# They also expect the petMar_lamp* databases in $(DATA_DIR)/ to prevent spew from makeblastdb
# In short these are pretty much a disparate set of targets from above.
# Naming convention is forward logical DNS to facilitate "obvious" autocompletion and discovery.

EVALUE = -evalue 1e-6
DATA_DIR = data
AS_TSV = -outfmt 6

# this is really just for my computer. there's no ./configure script so... oh well.
THREADED = -num_threads 8

BEST_MATCH = python best_match.py
TOTAL_MATCH = python total_match.py

lamp3.makeblastdb:
	makeblastdb -in $(DATA_DIR)/petMar_lamp3.fasta -dbtype nucl

lamp0.makeblastdb:
	makeblastdb -in $(DATA_DIR)/petMar_lamp0.fasta -dbtype nucl

p_marinus.rm_vlr:
	python lymphilter.py $(DATA_DIR)/p_marinus.cds.fa $(DATA_DIR)/p_marinus.no_vlr.cds.fa



p_marinus.x.lamp3: lamp3.makeblastdb
	blastn -db $(DATA_DIR)/petMar_lamp3.fasta -query $(DATA_DIR)/p_marinus.cds.fa $(EVALUE) $(AS_TSV) > p_marinus.x.lamp3.tsv

p_marinus.no_vlr.x.lamp3: lamp3.makeblastdb p_marinus.rm_vlr
	blastn -db $(DATA_DIR)/petMar_lamp3.fasta -query $(DATA_DIR)/p_marinus.no_vlr.cds.fa $(THREADED) $(EVALUE) $(AS_TSV) > $(DATA_DIR)/p_marinus.no_vlr.x.lamp3.tsv

p_marinus.no_vlr.x.lamp3.best_matches: p_marinus.no_vlr.x.lamp3
	$(BEST_MATCH) $(DATA_DIR)/p_marinus.no_vlr.x.lamp3.tsv $(DATA_DIR)/p_marinus.no_vlr.cds.fa > $(DATA_DIR)/p_marinus.no_vlr.x.lamp3.best_matches.tsv

p_marinus.no_vlr.x.lamp3.total_matches: p_marinus.no_vlr.x.lamp3
	$(TOTAL_MATCH) $(DATA_DIR)/p_marinus.no_vlr.x.lamp3.tsv $(DATA_DIR)/p_marinus.no_vlr.cds.fa > $(DATA_DIR)/p_marinus.no_vlr.x.lamp3.total_matches.tsv


p_marinus.x.lamp0: lamp0.makeblastdb
	blastn -db $(DATA_DIR)/petMar_lamp0.fasta -query $(DATA_DIR)/p_marinus.cds.fa $(EVALUE) $(AS_TSV) > p_marinus.x.lamp0.tsv

p_marinus.no_vlr.x.lamp0: lamp0.makeblastdb p_marinus.rm_vlr
	blastn -db $(DATA_DIR)/petMar_lamp0.fasta -query $(DATA_DIR)/p_marinus.no_vlr.cds.fa $(THREADED) $(EVALUE) $(AS_TSV) > $(DATA_DIR)/p_marinus.no_vlr.x.lamp0.tsv

p_marinus.no_vlr.x.lamp0.best_matches: p_marinus.no_vlr.x.lamp0
	$(BEST_MATCH) $(DATA_DIR)/p_marinus.no_vlr.x.lamp0.tsv $(DATA_DIR)/p_marinus.no_vlr.cds.fa > $(DATA_DIR)/p_marinus.no_vlr.x.lamp0.best_matches.tsv

p_marinus.no_vlr.x.lamp0.total_matches: p_marinus.no_vlr.x.lamp0
	$(TOTAL_MATCH) $(DATA_DIR)/p_marinus.no_vlr.x.lamp0.tsv $(DATA_DIR)/p_marinus.no_vlr.cds.fa > $(DATA_DIR)/p_marinus.no_vlr.x.lamp0.total_matches.tsv


lamp0.x.lamp3: lamp3.makeblastdb
	blastn -db $(DATA_DIR)/petMar_lamp0.fasta -query $(DATA_DIR)/petMar_lamp3.fasta $(THREADED) $(EVALUE) $(AS_TSV) > $(DATA_DIR)/lamp0.x.lamp3.tsv

lamp0.x.lamp3.best_matches: lamp0.x.lamp3
	$(BEST_MATCH) $(DATA_DIR)/lamp0.x.lamp3.tsv $(DATA_DIR)/petMar_lamp3.fasta > $(DATA_DIR)/lamp0.x.lamp3.best_matches.tsv

lamp0.x.lamp3.total_matches: lamp0.x.lamp3
	$(TOTAL_MATCH) $(DATA_DIR)/lamp0.x.lamp3.tsv $(DATA_DIR)/petMar_lamp3.fasta > $(DATA_DIR)/lamp0.x.lamp3.total_matches.tsv

