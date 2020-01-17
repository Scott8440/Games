from sfml import sf
import sfml
import random
import math

class Board:

  def __init__(self, width=600, height=600, title="", color="Black", frameRate=60):
    self.winWidth = width
    self.winHeight = height

    if (color.lower() == 'black'):
      self.bgColor = sf.Color.BLACK
    else:
      self.bgColor = sf.Color.WHITE

    self.window = sf.RenderWindow(sf.VideoMode(self.winWidth, self.winHeight), title)
    self.window.framerate_limit = frameRate 
 
  def displayBoard(self):
    self.window.display()

  def getBoundary(self):
    return (self.winWidth, self.winHeight)
