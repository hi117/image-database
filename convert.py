# converts a tdb to a kch
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

import pytc
from kyotocabinet import *
from sys import argv

if len(argv)!=3:
  print 'usage: python2 convert.py tdb kch'

tdb=pytc.BDB()
tdb.open(argv[1], pytc.BDBOWRITER | pytc.BDBOREADER | pytc.BDBOCREAT)
kdb=DB()
kdb.open(argv[2], DB.OWRITER | DB.OCREATE | DB.OREADER)
for key in tdb.keys():
  print key
  kdb.set(key,tdb.get(key))
