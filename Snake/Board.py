from sfml import sf
import sfml
import random
import math

class Board:
  

  def __init__(self, width=50, height=40, title="Snake", color="Black", squareSize=15, frameRate=20):
    self.width = width
    self.height = height
    self.winWidth = width*squareSize
    self.winHeight = height*squareSize

    if (color.lower() == 'black'):
      self.bgColor = sf.Color.BLACK
    else:
      self.bgColor = sf.Color.WHITE

    self.window = sf.RenderWindow(sf.VideoMode(self.winWidth, self.winHeight), title)
    self.window.framerate_limit = frameRate 
    self.squareSize = squareSize
    self.snake = None
    self.generateFood()
 
  def initSnake(self, snake):
    # takes a Snake object and adds it to the board
    self.snake = snake
 
  def generateFood(self, obj=None):
    while True: 
      position = (random.randint(0, self.width-1),
                  random.randint(0, self.height-1))
      if (not obj):
        self.food = position
        return
      repeat = False
      for square in obj.getHittableLocations():
        if square[0] == position[0] and square[1] == position[1]:
          repeat = True
      if (not repeat):
        break
    self.food = position

  def drawFood(self):
    food = sf.RectangleShape((self.squareSize,self.squareSize))
    food.fill_color = sf.Color.WHITE
    food.position = (self.food[0]*self.squareSize, self.food[1]*self.squareSize)
    self.window.draw(food)
  
  def drawBoard(self):
    self.window.clear(self.bgColor)
    self.drawFood()
  
  def displayBoard(self):
    self.window.display()

  def checkWallCollision(self, obj):
    return (obj[0] >= self.winWidth or
            obj[0] < 0 or
            obj[1] >= self.winHeight or
            obj[1] < 0) 

  def checkCollisions(self, obj):
    return self.checkWallCollision(obj)

  def handleKeyEvent(self, event):
    if (event.released):
      return
  
    if (event.code == sf.Keyboard.LEFT):
      self.snake.moveLeft()
    elif (event.code == sf.Keyboard.RIGHT):
      self.snake.moveRight()
    elif (event.code == sf.Keyboard.UP):
      self.snake.moveUp()
    elif (event.code == sf.Keyboard.DOWN):
      self.snake.moveDown()
  
  def checkEvents(self):
    for event in self.window.events:
      if type(event) is sf.CloseEvent:
        self.window.close()
        return False
      elif type(event) is sf.KeyEvent:
        self.handleKeyEvent(event)
    return True
