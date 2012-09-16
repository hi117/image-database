# extracts an image given a hash to directory
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

from sys import exit,argv
import pictures as p
import os
import os.path

def genPath(Hash):
    image=p._idb.images[Hash]
    return Hash+' - '+', '.join(image[2])+'.'+image[1].split(' ')[0]


if len(argv) != 4:
    print("usage: mass_extract.py db.ksh hash directory")
    exit(0)
if not os.path.isdir(argv[3]):
    print("error: pah given is dot a directory")
    exit(1)
p._idb=p.idb.db(argv[1])
os.chdir(argv[3])
open(genPath(argv[2]),'wb').write(p.extractImage(argv[2]))
