# this program extracts an entire database to a directory
# naming sceme is hash - tag, tag, tag.ext
from sys import exit,argv
import pictures as p
import os
import os.path

def genPath(Hash):
    image=p._idb.images[Hash]
    return Hash+' - '+', '.join(image[2])+'.'+image[1].split(' ')[0]

if len(argv) != 3:
    print("usage: mass_extract.py db.ksh directory")
    exit(0)
if not os.path.isdir(argv[2]):
    print("error: pah given is dot a directory")
    exit(1)
p._idb=p.idb.db(argv[1])
os.chdir(argv[2])
for picture in p.getImages():
    try:
        open(genPath(picture),'wb').write(p.extractImage(picture))
    except TypeError:
        print(picture)