# adds all files in the directory to the db
import pictures as p
from sys import argv,exit
import os
import os.path

if len(argv)!=3:
  print "Usage: python2 addall.py idb directory"
  exit(1)
p._idb=p.idb.db(argv[1])
# get a list of files in the directory
for i in os.listdir(argv[2]):
  if os.path.isfile(argv[2]+i):
    print "current path is: "+argv[2]+i
    p.add(argv[2]+i,'setMe')