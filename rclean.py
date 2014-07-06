# takes an argument of directory and image db and recursively removes images from the driectory already in the db
#
# Copyright (c) 2011 hi117
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
import os.path
from subprocess import check_output
from hashlib import sha1

if len(argv) != 3:
    print("Usage: python clean.py idb directory")
    exit(1)

p._idbi = p.idb.db(argv[1])

# get a list of files in the directory
images = p.getImages()
p.close()
del p

for i in check_output(['find', argv[2], '-type', 'f']).split("\n"):
    print("current path is: " + i)
    if os.path.isfile(i):
        Hash = sha1(open(i, 'rb').read()).hexdigest()
        if Hash in images:
            print("match: " + Hash)
            os.remove(i)
