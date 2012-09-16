This project requires python3, kyotocabinet, and kyotocabinet-python.
It is a personal project, do not expect it to be perfect.

To use it from an external program, run this sample code:
import pictures as p
p._idb=p.idb.db(dbLocation)

from there you can call functions in p to manipulate the database

to use the gui frontend, you need pygobject
to use it just run it with python gui.py
pictures.py and imageDB.py are libraries, the rest are programs using 
these libraries, each one has basic documentation in the top line of the program

TODO: 
redo some or all of the loops in gui.py
theyre truly terrible for what this database was meant to do
which is >1000 images per tag operations
some options are to redo in C or to find a better algorithm

Also creating a new database is broken last time i checked,
requires manual intervention to make a workable database 
due to how python handles pickling in 2 vs 3
