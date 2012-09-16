# counts the number of pictures in a db
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
