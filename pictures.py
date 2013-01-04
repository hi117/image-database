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

import imageDB as idb
#from types import StringType
import subprocess
from threading import Thread
from time import sleep
from pickle import dumps

StringType = type('')

'''
This file provides some common functions on the image db
'''

def _searchString(a):
    assert a in _idb.byTag
    o = {}
    for i in _idb.byTag[a]:
        o[i] = _idb.images[i]
    return o

def _searchStringHashes(a):
    assert a in _idb.byTag
    return list(_idb.byTag[a])

def _removeTag(a):
    assert a in _idb.byTag
    for Hash in _idb.byTag[a]:
        _idb.images[image][2].remove(a)

def _addTag(tag,hashes):
    if type(hashes) == StringType:
        _idb.addTag(hashes, tag)
        return

    _idb.addTag(hashes[0], tag)
    if len(hashes) == 1: return
    for Hash in hashes[1:]:
        _idb.addTag(Hash, tag)

def _searchHelper(job,tags,images):
    i = 0
    while i < len(job):
      image = job[i]
      for tag in tags:
          if not tag in images[image][2]:
            job.pop(i)
            break
      i += 1

def search(tags):
    '''
    This function searches the db for pictures matching all tags.
    '''
    if tags.__class__ == ''.__class__: return _searchString(tags)

    assert tags[0] in _idb.byTag,'does not exist'

    images = {}
    for i in _idb.byTag[tags[0]]:
      images[i] = _idb.images[i]

    if len(tags)==1: return images

    tags.pop(0)
    for image in list(images.keys()):
        for tag in tags:
            if not tag in images[image][2]:
                images.pop(image)
                break
    return images

def searchHashes(tags):
    '''
    This function is like search but returns a tag list.
    '''
    # Didnt I just define stringtype up there?
    if tags.__class__ == ''.__class__: return _searchStringHashes(tags)

    assert tags[0] in _idb.byTag,'does not exist'

    images = list(_idb.byTag[tags[0]])

    if len(tags) == 1: return images

    tags.pop(0)
    for image in images:
        for tag in tags:
            if not tag in images[image][2]:
                images.remove(image)
                break
    return images

def searchTop(tags,number):
    if tags.__class__ == ''.__class__: return _searchString(tags)

    assert tags[0] in _idb.byTag,'does not exist'

    images = {}
    for i in _idb.byTag[tags[0]]:
        images[i] = _idb.images[i]

    if len(tags) == 1: return list(images.keys())[:100]

    tags.pop(0)
    for image in images.keys():
        for tag in tags:
            if not tag in images[image][2]:
                images.remove(image)
                break
    return images

def add(path,tags):
    '''
    This function adds an image to the database with tag(s).
    '''
    if type(tags) == StringType: 
        _idb.addImage(path, tags)
        return

    Hash = _idb.addImage(path, tags[0])

    for i in tags[1:]:
        # add the remaining tags to the image
        _idb.addTag(Hash, i)
    return Hash

def remove(Hash):
    '''
    This function removes an inage from the database.
    '''
    _idb.rmImage(Hash)

def removeTag(tags):
    '''
    This function removes tag(s) from the database.
    '''
    if type(tags) == StringType:
        _removeTag(tags)
        return

    for tag in tags:
        _removeTag(tag)

def addTag(tags,hashes):
    '''
    This function adds the image(s) to the tag(s).
    '''
    if type(tags) == StringType:
        _addTag(tags.strip(), hashes)
        return

    for tag in tags:
        _addTag(tag.strip(), hashes)

def searchAll(tags):
    '''
    This function searches the db for pictures matching any tags.
    '''
    if type(tags) == StringType: return _searchString(tags)

    assert tags[0] in _idb.byTag, 'does not exist'

    images = {}
    for i in _idb.byTag[tags[0]]:
        images[i] = _idb.images[i]
    if len(tags) == 1: return images

    for tag in tags[1:]:
        tempImages = _searchString(tag)
        for i in tempImages:
            if not i in images:
                images.append(i)
    return images

def getTags():
    '''
    This function returns a list of tags.
    '''
    return list(_idb.byTag.keys())

def setTags(tags,Hash):
    '''
    This function sets the tags for an image.
    '''
    assert len(tags) > 0
    for tag in _idb.images[Hash][2]: # clear the current tag list
        _idb.byTag[tag.strip()].remove(Hash)

    _idb.images[Hash][2] = []
    for tag in tags:
        _addTag(tag.strip(),Hash)

    optimizeTags()

def optimizeTags():
    '''
    This function clears out unused tags from the database.
    '''
    for tag in list(_idb.byTag.keys()):
        if len(_idb.byTag[tag]) == 0:
            _idb.byTag.pop(tag)

def getTagsAll():
    '''
    This function returns all tags in the database.
    '''
    return _idb.byTag

def getImages():
    '''
    This function returns a list of hashes in the database.
    '''
    return _idb.images.keys()

def getImagesAll():
    '''
    This function returns all images in the database.
    '''
    return _idb.images

def close():
    '''
    This function closes the database.
    '''
    _idb.close()

def extractImage(Hash):
    '''
    This function extracts an image from the database.
    '''
    return _idb.getImage(Hash)
