mouse.protein.faa.psq: mouse.protein.faa
	formatdb -i mouse.protein.faa -o T -p T

lamp3.x.mouse: mouse.protein.faa.psq petMar_lamp3.fasta
	blastall -a 8 -i petMar_lamp3.fasta -d mouse.protein.faa -e 1e-3 -o lamp3.x.mouse -p blastx
