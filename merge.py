# takes 2 dbs and merges them into 1
#
# Copyright (c) 2011 Zachary Winnerman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
