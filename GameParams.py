 
class GameParams:
  
  boardWidth = 50
  boardHeight = 40
  squareSize = 15
  frameRate = 20
  
  def __init__(self, boardWidth=50, boardHeight=40, squareSize=15, frameRate=20):
    self.boardWidth = boardWidth
    self.boardHeight = boardHeight
    self.squareSize = squareSize
    self.frameRate = frameRate
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
