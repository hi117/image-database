# usage: python 4chdl.py imagedb board thread
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

from urllib.request import urlopen
from sys import argv
import json
import pictures as p
try:
    p._idb = p.idb.db(argv[1])
    thread = json.loads(str(urlopen('https://boards.4chan.org/'+argv[2] + '/res/' + argv[3] + '.json').read(), 'utf8'))
    for post in thread['posts']:
        if 'tim' in post:
            filename = str(post['tim']) + post['ext']
            print('downloading: ' + filename)
            try:
                p._idb.addImageB(urlopen('https://images.4chan.org/' + argv[2] + '/src/' + filename).read(), 'setMe')
            except AssertionError:
                print(filename + ' already exists!')
finally:
    p.close()
