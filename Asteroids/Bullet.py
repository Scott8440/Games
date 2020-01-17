from sfml import sf
import utils

class Bullet:
  
  def __init__(self, speed, position, boundary=None):
    
    self.velocity = speed
    self.boundary = boundary
    self.shape = sf.CircleShape()
    self.shape.radius = 2
    self.shape.fill_color = sf.Color.WHITE
    self.shape.position = position

  def draw(self, window):
    window.draw(self.shape) 
 
  def move(self):
    self.shape.position = (self.shape.position[0] + self.velocity[0], self.shape.position[1] + self.velocity[1])
  
  def shouldDelete(self):
    if not self.boundary:
      return False
    return (self.shape.position[0] < 0 
         or self.shape.position[1] < 0
         or self.shape.position[0] > self.boundary[0]
         or self.shape.position[1] > self.boundary[1]) 
  
  def getPosition(self):
    return utils.add2d(self.shape.position, (self.shape.radius, self.shape.radius))
