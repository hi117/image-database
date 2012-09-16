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

from kyotocabinet import *
from pickle import dumps,loads
from hashlib import sha1
from os.path import isfile
from subprocess import check_output
import tempfile

#pickle<{hash:[size,type,tags[]]}>
class db:
  def __init__(self,path):
    # initalize the db
    self._db =  DB()
    assert self._db.open(path, DB.OWRITER | DB.OREADER | DB.OCREATE),'error opening'
    # get and load the metadata entry
    #if not 'metadata' in self._db.match_prefix(''):
    if not self._db.check('metadata'):
      self._db.set('metadata',dumps({},0))
    self.images=loads(self._db.get('metadata'))
    self.byTag={}
    for k in self.images:
      v=self.images[k]
      for tag in v[2]:
        if not tag in self.byTag: self.byTag[tag]=[]
        self.byTag[tag].append(k)
  def addImage(self,path,initalTag):
    # add an image to the db
    imageHandle=open(path,'rb')
    image=imageHandle.read()
    imageHandle.close()
    Hash=sha1(image).hexdigest()
    assert not Hash in self.images, 'already exists'
    tmpImage=[len(image),str(check_output(["file","-b",path]),'utf8'),[initalTag]]
    # add the image to the db
    #self._db.set(Hash,open(path,'r').read())
    self._db.set(Hash,image)
    # add it to the listing
    self.images[Hash]=tmpImage
    if not initalTag in self.byTag: self.byTag[initalTag]=[]
    self.byTag[initalTag].append(Hash)
    # finally flush
    self.flush()
    return Hash
  def addImageB(self, image, initalTag):
    # adds an image from binary data
    Hash=sha1(image).hexdigest()
    assert not Hash in self.images, 'already exists'
    curImage=tempfile.NamedTemporaryFile(buffering=0)
    curImage.write(image)
    path=curImage.name
    tmpImage=[len(image),str(check_output(["file","-b",path]),'utf8'),[initalTag]]
    curImage.close()
    # add the image to the db
    #self._db.set(Hash,open(path,'r').read())
    self._db.set(Hash,image)
    # add it to the listing
    self.images[Hash]=tmpImage
    if not initalTag in self.byTag: self.byTag[initalTag]=[]
    self.byTag[initalTag].append(Hash)
    # finally flush
    self.flush()
    return Hash
  def rmImage(self,Hash):
    # remove an image from the db
    self._db.remove(Hash)
    tags=self.images[Hash][2]
    del self.images[Hash]
    for tag in tags:
      self.byTag[tag].remove(Hash)
    self.flush()
  def flush(self):
    # this updates the metadata in the db
    self._db.set('metadata',dumps(self.images))
  def close(self):
    self.flush()
    self.images={}
    self.path=""
    self.byTag={}
    self._db.close()
  def addTag(self,Hash, tag):
    # adds an existing image to a new tag
    assert Hash in self.images,'does not exist' # check if the image is actually here
    # check if the tag exists and create if if necessary
    if not tag in self.byTag: self.byTag[tag]=[]
    # add the image to the tag if necessary
    if not Hash in self.byTag[tag]: 
      self.byTag[tag].append(Hash)
      # update the image itself
      self.images[Hash][2].append(tag)
    self.flush()
  def rmTag(self,Hash, tag):
    # removes an existing image from a tag
    assert Hash in self.images, 'does not exist' # check if the image is actually here
    # remove the image from the tag if necessary
    if Hash in self.byTag[tag]: self.byTag[tag].remove(Hash)
    # update the image itself
    self.images[Hash][2].remove(tag)
    self.flush()
  def getImage(self,Hash):
    assert Hash in self.images,'does not exist'
    return self._db.get(Hash)
