from sfml import sf
from Asteroid import Asteroid
from Board import Board
from GameParams import GameParams
from ObjectManager import ObjectManager
from Powerup import Powerup
from ScoreKeeper import ScoreKeeper
from Ship import Ship
import utils

import random
import time

class AsteroidsGame:


  def setup(self, startWindow=None, playerName=None):
    self.params = GameParams() # To be filled by user input
    
    # Set up scorekeeping 
    self.score = 0
    self.scoreKeeper = ScoreKeeper()
    self.scoreKeeper.setFile('asteroidScore.txt')
 
    # Set up window
    width = 800
    height = 600
    font = sf.Font.from_file("rust.ttf")
    self.params.setFont(font) 

    if startWindow is None:
      # startWindow is None unless this is a restart
      startWindow = sf.RenderWindow(sf.VideoMode(width, height), "Asteroids")
      startWindow.framerate_limit = 60
      startWindow.clear(sf.Color.BLACK) 
 
      #Display Welcome
      welcomeText = utils.drawText(startWindow, string="Asteroids", size=60, font=font, position='center')
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
    difficulty = utils.selectOptions(startWindow, ["Easy", "Medium", "Hard"], [0, 1, 2], font)
    makeTimes = [20,15,12]
    timeModifiers = [0.98, 0.95, 0.92]
    self.params.setDifficulty(difficulty)
    self.timeToMakeAsteroid = makeTimes[difficulty]
    self.makeTimeModifier = timeModifiers[difficulty]
    self.lastAsteroidTime = time.time() - self.timeToMakeAsteroid

    self.timeToMakePowerup = 20
    self.lastPowerupTime = time.time() - self.timeToMakePowerup
    self.powerupProbability = 1/600
    
    # Set up Board
    self.board = Board(title="Asteroids", width=700, height=700)

    # Set up Ship
    self.ship = Ship(position=(self.board.getBoundary()[0]/2, self.board.getBoundary()[1]/2))
    self.ship.setWrapping(True)
    self.ship.setBoundary(self.board.getBoundary())
    
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
          self.setup(self.board.window, self.params.getPlayerName())
          self.playGame()

  def _generateAsteroid(self, asteroidManager, velocityLimit=2):
    if (time.time() - self.lastAsteroidTime >= self.timeToMakeAsteroid):
      self.lastAsteroidTime = time.time()
      self.timeToMakeAsteroid *= self.makeTimeModifier #make asteroids appear faster as time progresses
      
      # Generate beyond the border so it doesn't appear in middle of screen
      # random velocity will make it appear evenly on either side
      position = (random.uniform(-20, 0), random.uniform(-20,0))
      velocity = (random.uniform(-velocityLimit,velocityLimit),
                  random.uniform(-velocityLimit,velocityLimit))
      asteroid = Asteroid(4,position, velocity, wrapping=True, 
                          boundary=self.board.getBoundary()) 
      asteroidManager.addObject(asteroid)

  def _generatePowerup(self, powerupManager, velocityLimit=2):
    if ((time.time() - self.lastPowerupTime >= self.timeToMakePowerup) and
         random.random() < self.powerupProbability):
      
      typeNum = random.randint(0,2)
      typeNames = ["cooldown", "agility", "acceleration"]
      typeColors = [sf.Color.BLUE, sf.Color.GREEN, sf.Color.YELLOW]
      
      # Lots of calculations to make it start evenly on any side of the board
      # and ensure that it moves across the board no matter where it starts
      positionX = None
      positionY = None
      velocityX = None
      velocityY = None
      boundary = self.board.getBoundary()
      if random.random() < 0.5:
        positionX = random.uniform(-20, 0)
      else:
        positionX = random.uniform(boundary[0], boundary[0]+20)
      if random.random() < 0.5:
        positionY = random.uniform(-20, 0)
      else:
        positionY = random.uniform(boundary[0], boundary[0]+20)
      
      if (positionX < 0):
        velocityX =  random.uniform(0, velocityLimit)
      else:
        velocityX =  random.uniform(-velocityLimit, 0)
      if (positionY < 0):
        velocityY =  random.uniform(0, velocityLimit)
      else:
        velocityY =  random.uniform(-velocityLimit, 0)

       
       
      velocity = (velocityX, velocityY)
      position = (positionX, positionY)
      powerup = Powerup(position=position, velocity=velocity, 
                        color=typeColors[typeNum], powerupType=typeNames[typeNum])
      powerupManager.addObject(powerup)
      self.lastPowerupTime = time.time()
       
    
  def playGame(self):
    self.board.window.clear(sf.Color.BLACK)
    self.ship.draw(self.board.window)
    self.board.displayBoard()

    play = False
    while not play:
      for event in self.board.window.events: 
        if type(event) is sf.CloseEvent: 
          exit()
        elif (type(event) is sf.KeyEvent):
          play = True

    bulletManager = ObjectManager(cleanSize=10)
    asteroidManager = ObjectManager(cleanSize=10)
    powerupManager = ObjectManager(cleanSize=5)
    
    while(True): 
      self.board.window.clear(sf.Color.BLACK)
       
      self._generateAsteroid(asteroidManager)
      self._generatePowerup(powerupManager)

      # Input handler 
      for event in self.board.window.events:
        if type(event) is sf.CloseEvent:
          exit()
        if type(event) is sf.KeyEvent and event.code is sf.Keyboard.SPACE and event.pressed:
          bullet = self.ship.shootBullet(boundary=self.board.getBoundary())
          if bullet:
            bulletManager.addObject(bullet)
      if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
        self.ship.turnRight()
      if sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
        self.ship.accelerate()
      if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
        self.ship.turnLeft()
    
      # Move and draw bullets 
      for i in range(bulletManager.getLength()):
        bullet = bulletManager.getItem(i)
        bullet.move()
        bullet.draw(self.board.window)

      # Move and draw Asteroids
      for i in range(asteroidManager.getLength()):
        asteroid = asteroidManager.getItem(i)
        asteroid.move()
        asteroid.draw(self.board.window)
     
      # Move and draw Powerups
      for i in range(powerupManager.getLength()):
        powerup = powerupManager.getItem(i)
        powerup.move()
        powerup.draw(self.board.window)

      # Move and draw Ship    
      self.ship.moveForward()
      self.ship.draw(self.board.window)

      # Check for collisions
      newAsteroids = []
      for i in reversed(range(asteroidManager.getLength())):
        asteroid = asteroidManager.getItem(i) 
        # Asteroid-Ship collision
        if (self.ship.circleTriangleCollision(asteroid.getShape())):
          self.endGame()

        for j in reversed(range(bulletManager.getLength())):
          bullet = bulletManager.getItem(j)
          # if collision: break asteroid
          if asteroid.didCollide(bullet):
            self.score += 1
            if asteroid.breakAsteroid():
              for newAsteroid in asteroid.breakAsteroid():
                newAsteroids.append(newAsteroid)
            bulletManager.removeIndex(j)
            asteroidManager.removeIndex(i)
            break
      asteroidManager.addObjects(newAsteroids)
      
      # Check for powerup collisions
      for i in reversed(range(powerupManager.getLength())):
        powerup = powerupManager.getItem(i)
        if self.ship.circleTriangleCollision(powerup.getShape()):
          power = powerup.getType()
          if power == "acceleration":
            oldAcc = self.ship.getAcceleration()
            self.ship.setAcceleration(1.1*oldAcc) 
          elif power == "cooldown":
            oldCool = self.ship.getCooldown()
            self.ship.setCooldown(0.9*oldCool)
          elif power == "agility":
            oldSpeed = self.ship.getRotateSpeed()
            self.ship.setRotateSpeed(1.1*oldSpeed)
          powerupManager.removeIndex(i)
      
      self._drawScore(self.board.window)
      
      self.board.window.display()

  def _drawScore(self, window):
    if hasattr(self,'scoreText'):
      self.scoreText.string = str(self.score)
    else:
      self.scoreText = utils.drawText(window, size=25,
                         font=self.params.font, string=str(self.score))
    window.draw(self.scoreText)
