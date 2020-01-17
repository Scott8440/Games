from sfml import sf

class Paddle:
  
  def __init__(self, position=(0,0), boundary=(1000,500), width=20, height=5):
    
    self.width = width
    self.height = height
    self.boundary = boundary
    self.shape = sf.RectangleShape()
    self.shape.size = (width, height)
    self.shape.fill_color = sf.Color.WHITE
    self.position = (boundary[0]/2 - width/2, boundary[1]-height)
    self.shape.position = self.position 
    
    self.moveSpeed = 1
    
  def setMoveSpeed(self, speed):
    self.moveSpeed = speed
  
  def didCollide(self, ball):
    # Assuming ball is a sf.Rect
    
    position = ball.getPosition()
    size = ball.getSize()

    ballBottom = position[1]+size[1]
    ballLeft = position[0]
    ballRight = position[0] + size[0] 
    
    paddleTop = self.shape.position[1]
    paddleLeft = self.shape.position[0]
    paddleRight = self.shape.position[0] + self.width
   
    return (ballBottom >= paddleTop-1 and
            ballLeft < paddleRight and
            ballRight > paddleLeft) 
    
  def draw(self, window):
    self.shape.position = self.position
    window.draw(self.shape)
  
  def getShape(self):
    return self.shape
  
  def moveLeft(self):
    if self.position[0] >= 0:
      self.position = (self.position[0] - self.moveSpeed, self.position[1]) 

  def moveRight(self):
    if self.position[0] + self.width <= self.boundary[0]:
      self.position = (self.position[0] + self.moveSpeed, self.position[1]) 
