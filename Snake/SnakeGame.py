from Game import Game
from GameParams import GameParams
from ScoreKeeper import ScoreKeeper
from Board import Board
from snake import Snake
import utils
from sfml import sf
from sfml import system


class SnakeGame(Game):

  def setup(self, startWindow=None, playerName=None):
    
    self.score = 0
    self.scoreKeeper = ScoreKeeper()
    self.scoreKeeper.setFile('snakeScore.txt')
 
    self.params = GameParams() # To be filled by user input

    width = 800
    height = 600
    font = sf.Font.from_file("rust.ttf")

    if startWindow is None:
      # startWindow is None unless this is a restart
      startWindow = sf.RenderWindow(sf.VideoMode(width, height), "Snake")
      startWindow.framerate_limit = 60
      startWindow.clear(sf.Color.BLACK) 
 
      #Display Welcome
      welcomeText = utils.drawText(startWindow, string="Snake", size=60, font=font, position='center')
      startWindow.display()

        
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

    #TODO Choose PlayerName
    if playerName is None:
      playerName = utils.textInput(startWindow, "Enter Name:", font, maxLength=10)
    self.params.setPlayerName(playerName) 
    #Choose Difficulty
    difficulty = utils.selectOptions(startWindow, ["Easy", "Medium", "Hard"], [0, 1, 2], font)
    frameRates = [20, 25, 30]
    self.params.setDifficulty(difficulty)
    self.params.setFrameRate(frameRates[difficulty])
    #Choose Board Size
    boardSize = utils.selectOptions(startWindow, ["Small", "Medium", "Large"], [(40,30), (50,40), (60,50)], font)
    self.params.setBoardSize(boardSize)
    self.params.setSquareSize(15)
    
    self.params.setFont(font) 
    self.snake = Snake(5, self.params.squareSize, sf.Vector2(10,10))
    self.board = Board(width=self.params.boardWidth, height=self.params.boardHeight,
                       squareSize=self.params.squareSize, frameRate=self.params.frameRate)
    
    self.board.initSnake(self.snake)
    startWindow.close()
    self.playGame() 
 
  def endGame(self):
    gameOverText = utils.drawText(self.board.window, string="Game Over", font=self.params.font,
                   size=60, position='center', color=sf.Color.RED)
    
    oldScore = self.scoreKeeper.checkScore(self.params.playerName, self.params.getDifficulty())
    scoreTextYPosition = gameOverText.position[1]+gameOverText.local_bounds.height+10
    scoreText = None
    if self.score > oldScore:
      # display a "New Highscore" screen
      self.scoreKeeper.setScore(self.params.playerName, self.score, self.params.getDifficulty())
      
      utils.drawText(self.board.window, string="New High Score! {}".format(self.score),
                     font=self.params.font, size=30, position='center', yposition=scoreTextYPosition, color=sf.Color.GREEN)
    else:
      # Display the old highscore
      utils.drawText(self.board.window, string="High Score: {}".format(oldScore),
                     font=self.params.font, size=30, position='center', yposition=scoreTextYPosition, color=sf.Color.WHITE)
    
    utils.drawText(self.board.window, string="Press ENTER to Relplay",
                   font=self.params.font, size=15, position='center', yposition=self.board.window.height - 20, color=sf.Color.WHITE)
    
    self.board.window.display()
    while(True):
      for event in self.board.window.events:
        if (type(event) is sf.CloseEvent or
           (type(event) is sf.KeyEvent and event.code is sf.Keyboard.ESCAPE)):
          exit()  
        if (type(event) is sf.KeyEvent and event.code is sf.Keyboard.RETURN):
          # Reset
          self.snake = None
          self.setup(self.board.window, self.params.getPlayerName())


  def playGame(self):
    self.board.drawBoard()
    self.board.displayBoard()
    # wait for keypress to begin game
    play = False
    while not play:
      for event in self.board.window.events: 
        if type(event) is sf.CloseEvent: 
          exit()
        elif (type(event) is sf.KeyEvent):
          play = True

    while(True): 
      # Tell player to make their move
      self.snake.makeMove()
      # board should check if anything has been interacted with
        # call all of the checks (wall, self, food) and respond appropriately
      foundFood = self.snake.checkSquareCollision(self.board.food)
      if (foundFood):
        self.score += 1
        self.snake.addSquare()
        self.board.generateFood(self.snake)

      hitObject = (self.board.checkCollisions(self.snake.getHeadPosition()) or
                  self.snake.checkSelfCollision())
      if (hitObject):
        self.endGame()

      self.board.drawBoard() 
      self.snake.draw(self.board.window)
      self.drawScore(self.board.window)
      self.board.displayBoard()

      if not self.board.checkEvents():
        exit() 

  def drawScore(self, window):
    if hasattr(self,'scoreText'):
      self.scoreText.string = str(self.score)
    else:
      self.scoreText = utils.drawText(window, size=25,
                         font=self.params.font, string=str(self.score))
    window.draw(self.scoreText)

