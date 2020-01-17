 
class GameParams:
  
  
  def __init__(self, boardWidth=50, boardHeight=40, squareSize=15, frameRate=20, difficulty=0):
    self.boardWidth = boardWidth
    self.boardHeight = boardHeight
    self.squareSize = squareSize
    self.frameRate = frameRate
    self.difficulty = difficulty
    self.font = None
    self.playerName = None

  def setBoardSize(self, size):
    self.boardWidth = size[0]
    self.boardHeight = size[1] 

  def setFrameRate(self, rate):
    self.frameRate = rate

  def setSquareSize(self, size):
    self.squareSize = size
 
  def setFont(self, font):
    self.font = font
  
  def setPlayerName(self, name):
    self.playerName = name
  
  def getPlayerName(self):
    return self.playerName
  
  def setDifficulty(self, difficulty):
    self.difficulty = difficulty
  
  def getDifficulty(self):
    return self.difficulty
