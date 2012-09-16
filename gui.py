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

from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf
import os
import os.path
import tempfile
import pictures as p
from sys import argv
from pickle import dumps
import profile

def _getFileWrite(start=os.getcwd()):
  # displays a file selection dialog and returns the path to the file selected
  out=False
  dialog = gtk.FileChooserDialog("Extract..",
  None,
  gtk.FILE_CHOOSER_ACTION_SAVE,
  (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
  gtk.STOCK_OPEN, gtk.ResponseType.OK))
  dialog.set_default_response(gtk.ResponseType.OK)
  
  filter = gtk.FileFilter()
  filter.set_name("All files")
  filter.add_pattern("*")
  dialog.add_filter(filter)
  
  filter = gtk.FileFilter()
  filter.set_name("Images")
  filter.add_mime_type("image/png")
  filter.add_mime_type("image/jpeg")
  filter.add_mime_type("image/gif")
  filter.add_pattern("*.png")
  filter.add_pattern("*.jpg")
  filter.add_pattern("*.gif")
  filter.add_pattern("*.tif")
  filter.add_pattern("*.xpm")
  dialog.add_filter(filter)
  
  response = dialog.run()
  if response == gtk.ResponseType.OK:
    out= dialog.get_filename()
  elif response == gtk.ResponseType.CANCEL:
    out= False
  dialog.destroy()
  return out
def _getFile(start=os.getcwd()):
  # displays a file selection dialog and returns the path to the file selected
  out=False
  dialog = gtk.FileChooserDialog("Open..",
    None,
    gtk.FileChooserAction.OPEN,
    (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
    gtk.STOCK_OPEN, gtk.ResponseType.OK))
  dialog.connect("delete-event", gtk.main_quit)
  dialog.set_default_response(gtk.ResponseType.OK)
  filter = gtk.FileFilter()
  filter.set_name("All files")
  filter.add_pattern("*")
  dialog.add_filter(filter)
  filter = gtk.FileFilter()
  filter.set_name("Images")
  filter.add_mime_type("image/png")
  filter.add_mime_type("image/jpeg")
  filter.add_mime_type("image/gif")
  filter.add_pattern("*.png")
  filter.add_pattern("*.jpg")
  filter.add_pattern("*.gif")
  filter.add_pattern("*.tif")
  filter.add_pattern("*.xpm")
  dialog.add_filter(filter)
  response = dialog.run()
  if response == gtk.ResponseType.OK:
      out= dialog.get_filename()
  elif response == gtk.ResponseType.CANCEL:
      out= False
  dialog.destroy()
  return out
def getFile(title="Select File"):
    _result = False
    _fchooser = gtk.FileChooserDialog(title, None, gtk.FileChooserAction.OPEN,("Cancel", gtk.ResponseType.CANCEL,"Select File", gtk.ResponseType.OK))
    _fchooser.set_current_folder(os.path.expanduser("~"))
    _response = _fchooser.run()
    print('run passed')
    if _response == gtk.ResponseType.OK:
        _result = _fchooser.get_filename()
    _fchooser.destroy()
    del(_fchooser)
    return _result
def getFileWrite(title="Select File"):
    _result = False
    _fchooser = gtk.FileChooserDialog(title, None, gtk.FileChooserAction.SAVE,("Cancel", gtk.ResponseType.CANCEL,"Select File", gtk.ResponseType.OK))
    _fchooser.set_current_folder(os.path.expanduser("~"))
    _response = _fchooser.run()
    print('run passed')
    if _response == gtk.ResponseType.OK:
        _result = _fchooser.get_filename()
    _fchooser.destroy()
    del(_fchooser)
    return _result
class showStats:
  def delete_event(self, widget, event=None, data=None):
    gtk.main_quit()
    return False
  def __init__(self,button=None):
    def getSize():
      size=0
      for i in p._idb.images.keys():
        size+=p._idb.images[i][0]
      return size
    self.window = gtk.Window()
    self.window.connect("delete_event", self.delete_event)
    self.window.set_border_width(2)
    self.window.set_title("Image DB Stats")
    message="Images in db: "+str(len(p.getImages()))+'\n'
    message+="Size of metadata: "+str(len(dumps(p._idb.images)))+'\n'
    message+="Number of tags: "+str(len(p.getTags()))+'\n'
    message+="Number of unsorted images: "+str(len(p.search('setMe')))+'\n'
    message+="Theoretical size of DB: "+str(getSize())+'\n'
    message+="Percent Sorted: "+str(100-(((len(p.search('setMe'))*1.0)/len(p.getImages()))*100))+'\n'
    self.message=gtk.Label(message)
    self.window.add(self.message)
    self.message.show()
    self.window.show()
    gtk.main()
class mainWindow:
  def delete_event(self, widget, event, data=None):
    gtk.main_quit()
    return False
  def addPicture(self,button):
    # adds a picture from the filesystem to the database
    path=getFile()
    Hash=p.add(path,'setMe')
    # set the current image to this one after refreshing everything
    self.refreshTags()
    for button in self.pictures:
      if button.get_label()==Hash:
        button.toggled()
        break
  def removePicture(self,b):
    # removes a picture from the database given button
    for button in self.pictures[:]:
      if button.get_active():
        p.remove(button.get_label())
        break
    # refresh everything
    self.refreshTags()
    # set the active image to the one at the top of the list
    self.pictures[0].toggled()
  def extractPicture(self,button):
    # extracts a picture from the database to a given location
    path=getFileWrite()
    for button in self.pictures:
      if button.get_active():
        open(path,'wb').write(p.extractImage(button.get_label()))
        break
  def genSearch(self):
    # generates a search list from the state of the checkBoxes
    out=[]
    for i in self.checkBoxes:
      if i.get_active():
        out.append(i.get_label())
    return out
  def refreshTags(self):
    # refreshes the tag list
    curTags=p.getTags()
    for tag in self.checkBoxes[:]:
      gl=tag.get_label()
      if not gl in curTags:
        self.checkBoxesContainer.remove(tag)
        self.checkBoxes.remove(tag)
      else:
        curTags.remove(gl)
    for tag in curTags:
      b=gtk.CheckButton(label=tag)
      b.connect("toggled",self.checkSearch)
      b.show()
      self.checkBoxesContainer.pack_start(b,False,False,0)
      self.checkBoxes.append(b)
    self.checkSearch(True)
  def displayImage(self,button):
    # displays the image given a button
    Hash=button.get_label()
    curImage=tempfile.NamedTemporaryFile(buffering=0)
    curImage.write(p.extractImage(Hash))
    if 'GIF' in p._idb.images[Hash][1]:
        pixbuf = GdkPixbuf.PixbufAnimation.new_from_file(curImage.name)
        self.img.set_from_animation(pixbuf)
    else:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(curImage.name)
        size = self.img.get_allocation()
        imgSize = [pixbuf.get_width(),pixbuf.get_height()]
        # determine how to scale to keep aspect ratio
        wRatio=size.width/float(imgSize[0])
        hRatio=size.height/float(imgSize[1])
        if wRatio<hRatio:
            imgSize[0]=imgSize[0]*wRatio
            imgSize[1]=imgSize[1]*wRatio
        else:
            imgSize[0]=imgSize[0]*hRatio
            imgSize[1]=imgSize[1]*hRatio
        scaled_buf = pixbuf.scale_simple(int(imgSize[0]),int(imgSize[1]),GdkPixbuf.InterpType.HYPER)
        self.img.set_from_pixbuf(scaled_buf)
    curImage.close()
    # set the hash box to the correct value
    self.tagBar.set_text(', '.join(p.getImagesAll()[Hash][2]))
    self.tagBar.set_position(-1)
  def setPictures(self,hashes):
    # sets the hash list to a list as defined by hashes
    if len(self.pictureHashes)>500:
        print('cleaning cache')
        for i in self.pictures:
            self.pictureList.remove(i)
        self.pictureHashes=[]
        self.pictures=[]
    for i in self.pictures:
        i.hide()
    if not len(hashes): return
    for i in hashes:
        if not i in self.pictureHashes:
            if len(self.pictureHashes):
                b=gtk.RadioButton(group=self.pictures[0],label=i)
            else:
                b=gtk.RadioButton(label=i)
            b.connect("toggled",self.displayImage)
            b.show()
            self.pictureList.pack_start(b,False,False,0)
            self.pictures.append(b)
            self.pictureHashes.append(i)
    got=True
    for i in self.pictures:
        if i.get_label() in hashes:
            i.show()
            if got:
                i.clicked()
                i.toggled()
                got=False
  def checkSearch(self,button=None):
    # refreshes the hash list
    search=self.genSearch()
    if len(search)==0:
      self.setPictures([])
    else:
      if search==['setMe']:
        self.setPictures(sorted(p.searchTop(search,100)))
      else:
        self.setPictures(sorted(p.search(search).keys()))
    if self.autoFilterTagsCheckbox.get_active():
      self.autoFilterTags()
    return False
  def saveTags(self,button):
    # saves changes to the tagbar for an active image
    for button in self.pictures:
      if button.get_active():
        p.setTags(self.tagBar.get_text().split(','),button.get_label())
        break
    self.refreshTags()
    return False
  def autoFilterTags(self,button=None):
    # returns a list of tags based on the current state of the tag list
    # this list reflects different valid posibilities of tag combinations
    def _setMeHide(tag):
      if not tag.get_label()=='setMe':
        tag.hide()
    def _doubleLoopInner(i,tag):
      if i in p._idb.byTag[tag.get_label()]:
        tag.show()
    def _doubleLoopOuter(tag):
      tag.hide()
      list(map(_doubleLoopInner,a,[tag for x in range(len(self.checkBoxes))]))
    search=self.genSearch()
    if len(search)==0: 
      self.unfilterTags()
      return
    if search==['setMe']:
      list(map(_setMeHide,self.checkBoxes))
      return
    a=p.searchHashes(search)
    list(map(_doubleLoopOuter,self.checkBoxes))
  def unfilterTags(self):
    # shows all tags
    map(lambda tag: tag.show(),self.checkBoxes)
  def sortTags(self,button=None):
    # sorts the tags
    for tag in self.checkBoxes:
      self.checkBoxesContainer.remove(tag)
    self.checkBoxes=sorted(p.getTags())
    for tag in self.checkBoxes:
      b=gtk.CheckButton(label=tag)
      b.connect("toggled",self.checkSearch)
      b.show()
      self.checkBoxesContainer.pack_start(b,False,False,0)
  def __init__(self):
    #self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window = gtk.Window()
    self.window.connect("delete_event", self.delete_event)
    self.window.set_border_width(10)
    self.window.set_title("Image DB")
    self.window.set_size_request(800, 600)
    
    self.mainBox = gtk.VBox(False, 0) # contains the menubar and main panel
    self.barBox=gtk.HBox(False,0) # contains the menubar
    self.middleBox=gtk.HBox(False,0) # contains the main panel
    self.imageBox=gtk.VBox(False,0) # contains the image and the tag bar
    self.tagBox=gtk.HBox(False,0) # contains the tag bar and save button
    self.tagBar=gtk.Entry() # a bar editable to set the image's tags
    self.tagSave=gtk.Button(stock=gtk.STOCK_SAVE) # saves the image's tags
    self.bottomBox=gtk.HBox(False,0) # contains the bottom box for searching
    self.addButton=gtk.Button(label="Add",stock=gtk.STOCK_OPEN) # button to add a picture to the db
    self.extractBotton=gtk.Button(label="Extract",stock=gtk.STOCK_SAVE_AS) # button to extract a picture from the db
    self.removeButton=gtk.Button(label="Remove",stock=gtk.STOCK_STOP) # removes an image from the db
    self.statsButton=gtk.Button(label="Show Stats")
    self.autoFilterTagsCheckbox=gtk.CheckButton(label='Filter Tags')
    self.img=gtk.Image() # the image preview
    self.listBox=gtk.HBox(False,0) # a box to hold the lists on the left side
    self.checkBoxesContainerScroll=gtk.ScrolledWindow() # a scrollable area for the tags
    self.checkBoxesContainerScroll.set_border_width(0)
    self.checkBoxesContainer=gtk.VBox(False,0) # a box for the tags
    self.checkBoxes=[] # holds all the checkBoxes for tags
    self.pictureListScroll=gtk.ScrolledWindow() # a scrollable area for the hash list
    self.pictureList=gtk.VBox(False,0) # a box to hold the hashes
    self.pictures=[] # holds all the radio buttons for pictures
    self.pictureHashes=[] # holds the hashes in self.pictures
    
    # setup the top box's buttons
    self.addButton.connect("clicked",self.addPicture)
    self.extractBotton.connect("clicked",self.extractPicture)
    self.removeButton.connect("clicked",self.removePicture)
    self.statsButton.connect("clicked",showStats)
    self.barBox.pack_start(self.addButton,False,False,0)
    self.barBox.pack_start(self.extractBotton,False,False,0)
    self.barBox.pack_start(self.removeButton,False,False,0)
    self.barBox.pack_start(self.autoFilterTagsCheckbox,False,False,0)
    self.barBox.pack_start(self.statsButton,False,False,0)
    self.addButton.show()
    self.extractBotton.show()
    self.removeButton.show()
    self.autoFilterTagsCheckbox.show()
    self.statsButton.show()
    self.barBox.show()
    self.mainBox.pack_start(self.barBox,False,False,0)
    
    # setup the middle part's area
    for tag in sorted(p.getTags()):
      b=gtk.CheckButton(label=tag)
      b.connect("toggled",self.checkSearch)
      b.show()
      self.checkBoxesContainer.pack_start(b,False,False,0)
      self.checkBoxes.append(b)
    self.checkBoxesContainer.show()
    self.checkBoxesContainerScroll.add_with_viewport(self.checkBoxesContainer)
    self.checkBoxesContainerScroll.set_size_request(125,-1)
    self.checkBoxesContainerScroll.show()
    self.listBox.pack_start(self.checkBoxesContainerScroll,True,True,0)
    self.imageBox.pack_start(self.img,True,True,0)
    self.tagSave.connect("clicked",self.saveTags)
    self.tagBar.connect("activate",self.saveTags)
    self.img.show()
    self.tagBar.show()
    self.tagSave.show()
    self.tagBox.pack_start(self.tagBar,True,True,0)
    self.tagBox.pack_start(self.tagSave,False,False,0)
    self.tagBox.show()
    self.imageBox.pack_start(self.tagBox,False,False,0)
    self.pictureList.show()
    self.pictureListScroll.add_with_viewport(self.pictureList)
    self.pictureListScroll.show()
    self.listBox.pack_start(self.pictureListScroll,True,True,0)
    self.listBox.show()
    self.middleBox.pack_start(self.listBox,False,False,0)
    self.imageBox.show()
    self.middleBox.pack_start(self.imageBox,True,True,0)
    self.middleBox.show()
    self.mainBox.pack_start(self.middleBox,True,True,0)
    
    # leave out the bottom box for now
    # TODO make a bottom bar for more complex searches
    
    # finish setting up the display
    self.mainBox.show()
    self.window.add(self.mainBox)
    self.window.show()
    gtk.main()
if __name__=="__main__":
  if len(argv)>1:
    dbLocation=argv[1]
  else:
    dbLocation=getFile()
  try:  
    p._idb=p.idb.db(dbLocation)
    mainWindow()
  finally:
      p.close()
  #profile.run('mainWindow()')
