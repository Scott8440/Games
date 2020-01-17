# Objects in this list should implement a shouldDelete() function

class ObjectManager:
  
  def __init__(self, cleanSize=1000):
    
    self._list = []
    self._length = 0
    self._cleanSize = cleanSize #Size to clean up list at

  def addObject(self, obj):
    if obj == None:
      return
    self._list.append(obj)
    self._length += 1
    if self._length > self._cleanSize:
      self.cleanList()
  
  def addObjects(self, lst):
    if isinstance(lst, list):
      for i in range(len(lst)):
        self.addObject(lst[i])

  def removeObject(self, obj):
    for i in range(self._length):
      if self._list[i] == obj:
        del self._list[i]
        self._length -= 1
        return
  
  def removeIndex(self, index):
    if index < self._length:
      del self._list[index]
      self._length -= 1
  
  def removeItems(self, lst):
    for i in reversed(range(len(lst))):
      self.removeIndex(i)

  def cleanList(self):
    for i in reversed(range(self._length)):
      if self._list[i].shouldDelete():
        self.removeIndex(i) 

  def getLength(self):
    return self._length
  
  def getItem(self, index):
    return self._list[index]
  
  def getCleanSize(self):
    return self._cleanSize

  def setCleanSize(self, size):
    this._cleanSize = size
