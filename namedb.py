import cPickle
import screed

mouse_names = cPickle.load(open('mouse.namedb'))
mouse_fullname = cPickle.load(open('mouse.namedb.fullname'))
mouse_seqs = screed.ScreedDB('mouse.protein.faa')
