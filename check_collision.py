# takes an argument of directory and image db and prints images from the driectory already in the db
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
import os
import os.path
from hashlib import sha1

if len(argv) != 3:
    print "Usage: python check_collision.py idb directory"
    exit(1)

p._idb = p.idb.db(argv[1])

# get a list of files in the directory
for i in os.listdir(argv[2]):
    if os.path.isfile(argv[2] + i):
        Hash = sha1(open(argv[2] + i).read()).hexdigest()
        if Hash in p.getImages():
            print("match: " + Hash + ' ' + i)
