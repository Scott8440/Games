from Brick import Brick
from sfml import sf

class BrickWall:
  def __init__(self, boundary=((0,0),(100,100)), numWide=0, depth=0):
    self.bricks = []
    self.boundary = boundary
    self.width = numWide
    self.depth = depth
    
    self.layerHealth = {} # Store the health of each layer
   
  def setWallDepth(self, depth):
    self.depth = depth
  
  def setWallWidth(self, width):
    self.width = width
  
  def setLayerHealth(self, layer, health):
    self.layerHealth[layer] = health
  
  def setAllLayerHealth(self, health):
    for i in range(self.depth):
      self.layerHealth[i] = health
  
  def setLayerHealthGradient(self, minHealth, maxHealth):
    minHealth = max(1, minHealth) 
    maxHealth = max(minHealth, maxHealth) 

    for i in range(self.depth):
      health = minHealth + (i*(maxHealth - minHealth))//self.depth
      self.layerHealth[i] = health
 
  def createBricks(self):
    brickWidth = (self.boundary[1][0] - self.boundary[0][0]) / self.width
    brickHeight = (self.boundary[1][1] - self.boundary[0][1]) / self.depth

    for i in range(self.depth):
      layer = []
      yPos = self.boundary[0][1] + i*brickHeight
      for j in range(self.width):
        xPos = self.boundary[0][0] + j*brickWidth
        health = 0
        if i in self.layerHealth:
          health = self.layerHealth[i]
        else:
          health = self.depth - i        
        brick = Brick(position=(xPos,yPos), size=(brickWidth,brickHeight), health=health)
        layer.append(brick)
      self.bricks.append(layer)
    
  def getNumBricks(self):
    count = 0
    for layer in self.bricks:
      for brick in layer:
        count += 1
    return count
    
  def drawBricks(self, window):
    for layer in self.bricks:
      for brick in layer:
        brick.draw(window)

  def checkCollision(self, ball):
    for i in (range(len(self.bricks))):
      layer = self.bricks[i]
      for j in range(len(layer)): 
        brick = self.bricks[i][j]
        if brick.didCollide(ball):
          brick.damage()
          if brick.getHealth() == 0:
            del self.bricks[i][j]
          return brick
    return None

  
