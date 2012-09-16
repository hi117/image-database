# counts the number of pictures in a db
import pictures as p
from sys import argv,exit
from pickle import dumps

def getSize():
  size=0
  for i in p._idb.images.keys():
    size+=p._idb.images[i][0]
  return size

if len(argv)!=2:
  print("Usage: python2 addall.py idb")
  exit(1)
p._idb=p.idb.db(argv[1])
print("Images in db: ",len(p.getImages()))
print("Size of metadata: ",len(dumps(p._idb.images)))
print("Number of tags: ",len(p.getTags()))
print("Number of unsorted images: ",len(p.search('setMe')))
print("Theoretical size of DB: ",getSize())
print("Percent Sorted: ",100-(((len(p.search('setMe'))*1.0)/len(p.getImages()))*100))
