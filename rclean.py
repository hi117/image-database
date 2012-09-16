# takes an argument of directory and image db and recursively removes images from the driectory already in the db
import pictures as p
from sys import argv,exit
import os.path
from subprocess import check_output
from hashlib import sha1

if len(argv)!=3:
  print "Usage: python2 clean.py idb directory"
  exit(1)
p._idb=p.idb.db(argv[1])
# get a list of files in the directory
#for i in os.listdir(argv[2]):
images=p.getImages()
p.close()
del p
for i in check_output(['find',argv[2],'-type','f']).split("\n"):
  print "current path is: "+i
  if os.path.isfile(i):
    Hash=sha1(open(i).read()).hexdigest()
    if Hash in images:
      print "match: "+Hash
      os.remove(i)