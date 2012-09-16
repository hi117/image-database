# takes an argument of directory and image db and removes images from the driectory already in the db
import pictures as p
from sys import argv,exit
import os
import os.path
from hashlib import sha1

if len(argv)!=3:
  print "Usage: python2 clean.py idb directory"
  exit(1)
p._idb=p.idb.db(argv[1])
# get a list of files in the directory
for i in os.listdir(argv[2]):
  print "current path is: "+argv[2]+i
  if os.path.isfile(argv[2]+i):
    Hash=sha1(open(argv[2]+i).read()).hexdigest()
    if Hash in p.getImages():
      print "match: "+Hash
      os.remove(argv[2]+i)