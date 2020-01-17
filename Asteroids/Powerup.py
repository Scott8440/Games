from sfml import sf
import time
import utils

class Powerup:
  def __init__(self, color=sf.Color.GREEN, position=(0,0), velocity=(1,1), powerupType="none"):
    
    self.powerupType = powerupType
    
    self.lifetime = 20
    self.creationTime = time.time()
    
    self.position = position
    self.velocity = velocity
    
    self.shape = sf.CircleShape(8)
    self.shape.position = self.position
    self.shape.fill_color = color
    
  def getShape(self):
    return self.shape
  
  def draw(self, window):
    self.shape.position = self.position
    window.draw(self.shape)
    
  def move(self):
    self.position = utils.add2d(self.position, self.velocity) 
  
  def getType(self):
    return self.powerupType
  
  def shouldDelete(self):
    # If time is later than lifetime
    return time.time() - self.creationTime > self.lifetime
