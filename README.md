This project requires kyotocabinet kyotocabinet-python.
It is a personal project, do not expect it to be perfect.

To use it from an external program, run this sample code:
import pictures as p
p._idb=p.idb.db(dbLocation)

from there you can call functions in p to manipulate the database

to use the gui frontend, you need pygobject
to use it just run it with python gui.py
pictures.py and imageDB.py are libraries, the rest are programs using 
these libraries, each one has basic documentation in the top line of the program
