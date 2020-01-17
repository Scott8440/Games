from sfml import sf
from utils import Directions

class Snake:

  def __init__(self, length, size, startingPosition):
    
    self.snakeLocations = [] 
    self.moving = Directions.RIGHT 
    self.size = size 
    self.length = length
    for i in range(length):
      self.snakeLocations.append((startingPosition.x - i,
                                  startingPosition.y)) 
    
  def getHittableLocations(self):
    return self.snakeLocations

  def addSquare(self):
    tail = self.snakeLocations[0] 
    modifier = self.directionToModifier(self.moving)
    self.snakeLocations.insert(0, (tail[0] + modifier['x'],
                                   tail[1] + modifier['y'])) 
    self.length += 1

  def makeMove(self):
    # head moves in direction, everything else moves to where the one in front
    # of it was
    
    head = self.snakeLocations[0]
    for i in range(self.length-1,0, -1): 
      self.snakeLocations[i] = self.snakeLocations[i-1]
    
    modifier = self.directionToModifier(self.moving)
    self.snakeLocations[0] = (head[0] + modifier['x'],
                              head[1] + modifier['y']) 
  
  def draw(self, window):
    for snakeSquare in self.snakeLocations:
      square = sf.RectangleShape((self.size-1, self.size-1))
      square.fill_color = sf.Color.WHITE
      square.position = (snakeSquare[0]*self.size, snakeSquare[1]*self.size)    
      window.draw(square)
  
  def getHeadPosition(self):
    head = self.snakeLocations[0]
    return (head[0]*self.size, head[1]*self.size)
  
  def checkSelfCollision(self):
    head = self.snakeLocations[0]
    for i in range(1, self.length):
      if self.checkSquareCollision(self.snakeLocations[i]):
        return True

  def checkSquareCollision(self, position, size=1):
    head = self.snakeLocations[0]
    return (head[0] > position[0] - size and
            head[0] < position[0] + size and
            head[1] > position[1] - size and
            head[1] < position[1] + size)
    
  def directionToModifier(self, direction):
    if direction == Directions.RIGHT:
      return {'x': 1, 'y': 0}
    elif direction == Directions.LEFT:
      return {'x': -1, 'y': 0}
    elif direction == Directions.UP:
      return {'x': 0, 'y': -1}
    else:
      return {'x': 0, 'y': 1} 

  def moveLeft(self):
    if self.moving != Directions.RIGHT:
      self.moving = Directions.LEFT
  def moveRight(self):
    if self.moving != Directions.LEFT:
      self.moving = Directions.RIGHT
  def moveUp(self):
    if self.moving != Directions.DOWN:
      self.moving = Directions.UP
  def moveDown(self):
    if self.moving != Directions.UP:
      self.moving = Directions.DOWN
