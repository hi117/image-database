# usage: python 4chdl.py imagedb url
from urllib.request import urlopen
from sys import argv
import json
import pictures as p
try:
    p._idb=p.idb.db(argv[1])
    p._idb.addImageB(urlopen(argv[2]).read(),'setMe')
finally:
    p.close()