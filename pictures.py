import imageDB as idb
#from types import StringType
import subprocess
from threading import Thread
from time import sleep
from pickle import dumps

StringType=type('')
# this file provides some common functions on the image db
def _searchString(a):
  assert a in _idb.byTag
  o={}
  for i in _idb.byTag[a]:
    o[i]=_idb.images[i]
  return o
def _searchStringHashes(a):
  assert a in _idb.byTag
  return list(_idb.byTag[a])
def _removeTag(a):
  assert a in _idb.byTag
  for Hash in _idb.byTag[a]:
    _idb.images[image][2].remove(a)
def _addTag(tag,hashes):
  if type(hashes)==StringType:
    _idb.addTag(hashes,tag)
    return
  _idb.addTag(hashes[0],tag)
  if len(hashes)==1: return
  for Hash in hashes[1:]:
    _idb.addTag(Hash,tag)
def _searchHelper(job,tags,images):
  #for image in job:
  i=0
  while i < len(job):
    image=job[i]
    for tag in tags:
      if not tag in images[image][2]:
        job.pop(i)
        break
    i+=1
def search(tags):
  # searches the db for pictures matching all tags
  if tags.__class__ == ''.__class__: return _searchString(tags)
  assert tags[0] in _idb.byTag,'does not exist'
  images={}
  for i in _idb.byTag[tags[0]]:
    images[i]=_idb.images[i]
  if len(tags)==1: return images
  tags.pop(0)
  for image in list(images.keys()):
    for tag in tags:
      #if not tag in images[i][2]:
      if not tag in images[image][2]:
        images.pop(image)
        break
  return images
def searchHashes(tags):
  # like search but returns a tag list
  if tags.__class__ == ''.__class__: return _searchStringHashes(tags)
  assert tags[0] in _idb.byTag,'does not exist'
  images=list(_idb.byTag[tags[0]])
  if len(tags)==1: return images
  tags.pop(0)
  for image in images:
    for tag in tags:
      #if not tag in images[i][2]:
      if not tag in images[image][2]:
        images.remove(image)
        break
  return images
def searchTop(tags,number):
  if tags.__class__ == ''.__class__: return _searchString(tags)
  assert tags[0] in _idb.byTag,'does not exist'
  images={}
  for i in _idb.byTag[tags[0]]:
    images[i]=_idb.images[i]
  #open('out','w').write(dumps(images))
  if len(tags)==1: return list(images.keys())[:100]
  tags.pop(0)
  for image in images.keys():
    for tag in tags:
      #if not tag in images[i][2]:
      if not tag in images[image][2]:
        images.remove(image)
        break
  return images
def add(path,tags):
  # add an image to the database with tag(s)
  if type(tags) == StringType: 
    _idb.addImage(path,tags)
    return
  Hash=_idb.addImage(path,tags[0])
  for i in tags[1:]:
    # add the remaining tags to the image
    #_idb.images[Hash][2].append(i)
    #print i
    _idb.addTag(Hash,i)
  return Hash
def remove(Hash):
  # remove an inage from the database
  _idb.rmImage(Hash)
def removeTag(tags):
  # removes tag(s) from the database
  if type(tags)==StringType:
    _removeTag(tags)
    return
  for tag in tags:
    _removeTag(tag)
def addTag(tags,hashes):
  # adds the image(s) to the tag(s)
  if type(tags)==StringType:
    _addTag(tags.strip(),hashes)
    return
  for tag in tags:
    _addTag(tag.strip(),hashes)
def searchAll(tags):
  # searches the db for pictures matching any tags
  if type(tags) == StringType: return _searchString(tags)
  assert tags[0] in _idb.byTag,'does not exist'
  images={}
  for i in _idb.byTag[tags[0]]:
    images[i]=_idb.images[i]
  if len(tags)==1: return images
  for tag in tags[1:]:
    tempImages=_searchString(tag)
    for i in tempImages:
      if not i in images:
        images.append(i)
  return images
def getTags():
  # return a list of tags
  return list(_idb.byTag.keys())
def setTags(tags,Hash):
  # sets the tags for an image
  assert len(tags)>0
  for tag in _idb.images[Hash][2]: # clear the current tag list
    _idb.byTag[tag.strip()].remove(Hash)
  _idb.images[Hash][2]=[]
  for tag in tags:
    _addTag(tag.strip(),Hash)
  optimizeTags()
def optimizeTags():
  # this function clears out unused tags from the database
  for tag in list(_idb.byTag.keys()):
    if len(_idb.byTag[tag])==0:
      del _idb.byTag[tag]
def getTagsAll():
  # return all tags
  return _idb.byTag
def getImages():
  # return a list of hashes
  return _idb.images.keys()
def getImagesAll():
  # return all images
  return _idb.images
def close():
  # closes the db
  _idb.close()
def extractImage(Hash):
  # extracts an image from the database
  return _idb.getImage(Hash)
def searchEx(a):
  # searches using an expressino
  # |=or &=and 
  #TODO () are honored
  a.split('[&]|[|]')
#_idb=idb.db('pictures.tdb')