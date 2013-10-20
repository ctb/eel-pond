import cPickle
import screed

fp = open('mouse.namedb')
is_ncbi = cPickle.load(fp)
mouse_names = cPickle.load(fp)
fp.close()

mouse_fullname = cPickle.load(open('mouse.namedb.fullname'))
mouse_seqs = screed.ScreedDB('mouse.protein.faa')
