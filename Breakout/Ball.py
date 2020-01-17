from sfml import sf
import utils
import random
import math

class Ball:
  def __init__(self, position=(0,0), speed=3, direction=325, color=sf.Color.WHITE):
    
    self.shape = sf.RectangleShape()
    self.shape.size = (3,3)
    self.shape.fill_color = color
    
    self.position = position
    self.speed = speed
    self.direction = direction # Measured in degrees from horizontal
    self.velocity = self.getVelocity()
    
    self.lastFramePosition = None
   
  def getVelocity(self):
    return (self.speed*math.cos((math.pi/180*self.direction)),
            self.speed*math.sin((math.pi/180*self.direction)))
   
  def draw(self, window):
    
    self.shape.position = self.position
    window.draw(self.shape)
  
  def getPosition(self):
    return self.shape.position
 
  def getSize(self):
    return self.shape.size
  
  def move(self):
    self.lastFramePosition = self.position
    self.position = utils.add2d(self.position, self.getVelocity())
  
  def bounceVertical(self, angleFromVertical=None):
    prevVelocity = self.getVelocity()
    self.direction = -self.direction % 360
    # angle from vertical:
    if angleFromVertical is not None:
      print("Angle: {}".format(angleFromVertical))
      sign = 1
      if self.direction > 270:
        sign = -1
      # if negative, move ccw (positive) to make more vertical
      self.direction = 270 - sign*angleFromVertical 
      if (prevVelocity[1] < 0): # if it was moving up flip it back down
        print("flip again")
        self.direction = -self.direction % 360
      
  
  def bounceHorizontal(self, degree=0):
    self.direction = (180 - self.direction) % 360
  
  def rectangleBounce(self, rect):
    # To handle bouncing off of a sf.RectangleShape where the angle depends
    # on which part of the rectangle was hit
    
    rectLeft = rect.position[0]
    rectRight = rect.position[0]+rect.size[0]
    rectBottom = rect.position[1] + rect.size[1]
    rectTop = rect.position[1]
    
    selfCenter = self.position[0] + self.shape.size[0]/2
    relativeX = selfCenter - rectLeft
    relativeXRatio = relativeX/rect.size[0]

    # handle side collisions
    lastFrameX = self.lastFramePosition[0] + self.shape.size[1]/2
    lastFrameY = self.lastFramePosition[1] + self.shape.size[1]/2
    
    
    degreeFromVertical = None 
    # If from the right, was withinY, but >X
    if (lastFrameY > rectTop and lastFrameY < rectBottom):
      self.bounceHorizontal() 
      return
    
    if relativeXRatio > 0.75:
      # Hit right end
      if self.getVelocity()[0] < 0: # Moving left
        self.bounceHorizontal()
      degreeFromVertical = 60
    elif relativeXRatio < 0.25:
      # Hit left end
      if self.getVelocity()[0] > 0: # Moving Right
        self.bounceHorizontal()
      degreeFromVertical = 60
    else:
      # Hit middle
      degreeFromVertical = 45
    
    self.bounceVertical(degreeFromVertical)
