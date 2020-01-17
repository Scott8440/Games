from sfml import sf
from sfml import system

from Ball import Ball
from Brick import Brick
from BrickWall import BrickWall
from Board import Board
from GameParams import GameParams
from ObjectManager import ObjectManager
from Paddle import Paddle
from ScoreKeeper import ScoreKeeper
import utils

import random
import time

class BreakoutGame:

  def setup(self, startWindow=None, playerName=None):
    self.params = GameParams() # To be filled by user input
    
    # Set up scorekeeping 
    self.score = 0
    self.scoreKeeper = ScoreKeeper()
    self.scoreKeeper.setFile('breakoutScore.txt')
 
    # Set up window
    width = 800
    height = 600
    font = sf.Font.from_file("rust.ttf")
    self.params.setFont(font) 

    if startWindow is None:
      # startWindow is None unless this is a restart
      startWindow = sf.RenderWindow(sf.VideoMode(width, height), "Breakout")
      startWindow.framerate_limit = 60
      startWindow.clear(sf.Color.BLACK) 
 
      #Display Welcome
      welcomeText = utils.drawText(startWindow, string="Breakout", size=60, font=font, position='center')
      startWindow.display()
        
    # Wait for any input
    while(True):
      setup = False
      for event in startWindow.events: 
        if type(event) is sf.CloseEvent: 
          exit()
        elif (type(event) is sf.MouseButtonEvent or
              type(event) is sf.KeyEvent):
            setup = True 
      if setup:
        break

    # Select Player Name
    if playerName is None:
      playerName = utils.textInput(startWindow, "Enter Name:", font, maxLength=10)
    self.params.setPlayerName(playerName.lower()) 

    #Choose Difficulty
    #difficulty = utils.selectOptions(startWindow, ["Easy", "Medium", "Hard"], [0, 1, 2], font)
    #self.params.setDifficulty(difficulty)

    # Set up Board
    self.board = Board(title="Breakout", width=1000, height=500)

    # Set up Paddle
    self.paddle = Paddle(boundary=self.board.getBoundary(), width=75, height=15)
    self.paddle.setMoveSpeed(10)
    
    # Gameplay parameters
    self.maxLayers = 5
    self.level = 1
    
    startWindow.close()
 
  def endGame(self):
    gameOverText = utils.drawText(self.board.window, string="Game Over", font=self.params.font,
                   size=60, position='center', color=sf.Color.RED)
    
    oldScore = self.scoreKeeper.checkScore(self.params.playerName, self.params.getDifficulty())
    scoreTextYPosition = gameOverText.position[1]+gameOverText.local_bounds.height+10

    if self.score > oldScore:
      # display a "New Highscore" screen
      self.scoreKeeper.setScore(self.params.playerName, self.score, self.params.getDifficulty())
      
      utils.drawText(self.board.window, string="New High Score! {}".format(self.score),
                     font=self.params.font, size=30, position='center', 
                     yposition=scoreTextYPosition, color=sf.Color.GREEN)
    else:
      # Display the old highscore
      utils.drawText(self.board.window, string="High Score: {}".format(oldScore),
                     font=self.params.font, size=30, position='center', 
                     yposition=scoreTextYPosition, color=sf.Color.WHITE)
    
    utils.drawText(self.board.window, string="Press ENTER to Relplay",
                   font=self.params.font, size=15, position='center', 
                   yposition=self.board.window.height - 20, color=sf.Color.WHITE)
    
    self.board.window.display()
    while(True):
      for event in self.board.window.events:
        if (type(event) is sf.CloseEvent or
           (type(event) is sf.KeyEvent and event.code is sf.Keyboard.ESCAPE)):
          exit()  
        if (type(event) is sf.KeyEvent and event.code is sf.Keyboard.RETURN):
          # Reset
          self.board.window.clear(sf.Color.BLACK)
          self.setup(self.board.window, self.params.getPlayerName())
          self.playGame()
  
  def playLevel(self, level):
    self.board.window.clear(sf.Color.BLACK)
    self.paddle.draw(self.board.window)

    self.board.displayBoard()

    play = False
    while not play:
      for event in self.board.window.events: 
        if type(event) is sf.CloseEvent: 
          exit()
        elif (type(event) is sf.KeyEvent):
          play = True

    ballManager = ObjectManager(cleanSize=10)
    
    screenWidth = self.board.getBoundary()[0]
    screenHeight =  self.board.getBoundary()[1]
 
    
    # Calculate BrickWall difficulty parameters 
    wallDepth = min(self.maxLayers, self.level)
    wallLength = 10 + 2*(self.level // 5) # increase by 2 width every 5 levels
    
    boundary = ((0, 25),(screenWidth, 25 + min(20*wallDepth, screenHeight/3)))
    
    brickWall = BrickWall(boundary=boundary)
    brickWall.setWallDepth(wallDepth)
    brickWall.setWallWidth(wallLength)
    
    if self.level < self.maxLayers: # Set all bricks health = 1
      brickWall.setAllLayerHealth(1)
    else:
      minHealth = 1 + (self.level // 3)
      maxHealth = self.maxLayers + (self.level // 3)
      brickWall.setLayerHealthGradient(minHealth, maxHealth)
    
    brickWall.createBricks()
    
    ballSpeed = 4.5 + 0.2*self.level

    ball = Ball(position=(100,screenHeight/2), speed=ballSpeed, direction=45)
    ballManager.addObject(ball)
    
    while(True): 
      self.board.window.clear(sf.Color.BLACK)
       
      # Input handler 
      for event in self.board.window.events:
        if type(event) is sf.CloseEvent:
          exit()
        if type(event) is sf.KeyEvent and event.pressed and (event.code is sf.Keyboard.RETURN):
          self.level += 1
          self.playLevel(self.level)
      if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
        self.paddle.moveRight()
      if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
        self.paddle.moveLeft()
    
      # Move and draw balls
      for i in range(ballManager.getLength()):
        ball = ballManager.getItem(i)
        ball.move()
        ball.draw(self.board.window)

      # Draw bricks
      brickWall.drawBricks(self.board.window)

      # Draw Paddle    
      self.paddle.draw(self.board.window)

      # Check for Ball-Brick Collisions
      for i in range(ballManager.getLength()):
        ball = ballManager.getItem(i)
        brick = brickWall.checkCollision(ball)
        if brick:
          ball.rectangleBounce(brick.getShape()) 
          if (brick.getHealth() == 0): 
            self.score += 1

      # Check for Ball Collisions
      for i in range(ballManager.getLength()):
        ball = ballManager.getItem(i)
        position = ball.getPosition()
        size = ball.getSize()
        if self.paddle.didCollide(ball):
          ball.rectangleBounce(self.paddle.getShape())
        # Check for Ball-Wall Collision
        if (position[0] <= 0 or
            position[0] + size[0] >= self.board.getBoundary()[0]):
          ball.bounceHorizontal()
        if (position[1] <= 0):
          ball.bounceVertical()
        # Remove Dead Balls
        deadBalls = []
        if (position[1] >= self.board.getBoundary()[1]):
          deadBalls.append(i)
        ballManager.removeItems(deadBalls)
        
        # Check if any balls left
        if ballManager.getLength() == 0:
          self.endGame()
        
        # Check if any bricks left
        if brickWall.getNumBricks() == 0:
          self.level += 1
          self.playLevel(self.level)
 
      self._drawScore(self.board.window)
      self.board.window.display()
     
  def playGame(self):
    self.playLevel(self.level) 

  def _drawScore(self, window):
    if hasattr(self,'scoreText'):
      self.scoreText.string = str(self.score)
    else:
      self.scoreText = utils.drawText(window, size=25,
                         font=self.params.font, string=str(self.score))
    window.draw(self.scoreText)
