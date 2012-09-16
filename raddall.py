# recursively adds all files in the directory to the db
import pictures as p
from sys import argv,exit
from subprocess import check_output
import os.path

if len(argv)!=3:
  print "Usage: python2 addall.py idb directory"
  exit(1)
p._idb=p.idb.db(argv[1])
# get a list of files in the directory
#for i in os.listdir(argv[2]):
for i in check_output(['find',argv[2],'-type','f']).split("\n"):
  if os.path.isfile(i):
    print "current path is: "+i
    try:
      p.add(i,'setMe')
    except AssertionError as e:
      print "match: "+i