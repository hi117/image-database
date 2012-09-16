# usage: python 4chdl.py imagedb board thread
from urllib.request import urlopen
from sys import argv
import json
import pictures as p
try:
    p._idb=p.idb.db(argv[1])
    thread = json.loads(str(urlopen('https://boards.4chan.org/'+argv[2]+'/res/'+argv[3]+'.json').read(),'utf8'))
    for post in thread['posts']:
        if 'tim' in post:
            filename=str(post['tim'])+post['ext']
            print('downloading: '+filename)
            p._idb.addImageB(urlopen('https://images.4chan.org/'+argv[2]+'/src/'+filename).read(),'setMe')
finally:
    p.close()