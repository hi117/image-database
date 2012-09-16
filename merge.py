# takes 2 dbs and merges them into 1
import pictures as p
import tempfile
from sys import argv

if len(argv)!=3:
  print "Usage: python2 addall.py idb1 idb2"
  exit(1)
p1=p.pictures()
p2=p.pictures()
p1._idb=p.idb.db(argv[1])
p2._idb=p.idb.db(argv[2])

for i in p1.getImages():
  print "current image "+i
  curImage=tempfile.NamedTemporaryFile(bufsize=0)
  curImage.write(p1.extractImage(i))
  try:
    p2.add(curImage.name,p1._idb.images[i][2])
  except AssertionError as e:
    print "match: "+i
  curImage.close()
p1.close()
p2.close()