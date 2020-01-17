from sfml import sf

class Brick:
  
  colors = [sf.Color.WHITE, sf.Color.BLUE, sf.Color.GREEN, 
            sf.Color.YELLOW, sf.Color.RED]
  
  def __init__(self, position=(0,0), size=(10,3), health=1):
    
    self.shape = sf.RectangleShape()
    self.shape.position = position
    self.shape.size = size
    self.shape.outline_thickness=1
    self.shape.outline_color = sf.Color.BLACK
    
    self.health = health
  
  def draw(self,window):
    index = min(len(self.colors)-1, self.health)
    self.shape.fill_color = self.colors[index]
    window.draw(self.shape)
  
  def getShape(self):
    return self.shape
  
  def getHealth(self): 
    return self.health
  
  def didCollide(self, ball):
    position = ball.getPosition()
    size = ball.getSize()

    ballTop = position[1]
    ballBottom = position[1]+size[1]
    ballLeft = position[0]
    ballRight = position[0] + size[0]

    brickBottom = self.shape.position[1] + self.shape.size[1]
    brickTop = self.shape.position[1]
    brickLeft = self.shape.position[0]
    brickRight = self.shape.position[0] + self.shape.size[0]

    return (ballBottom >= brickTop-1 and
            ballTop <= brickBottom+1 and
            ballLeft < brickRight and
            ballRight > brickLeft)
  
 
  def damage(self, damage=1):
    self.health = max(0, self.health - damage)

