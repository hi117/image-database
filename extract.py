# extracts an image given a hash to directory
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