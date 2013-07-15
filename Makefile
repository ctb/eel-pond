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

