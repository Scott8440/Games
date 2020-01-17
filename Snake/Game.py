from sfml import sf
from sfml import system
from ScoreKeeper import ScoreKeeper
from GameParams import GameParams

# A base Game class which all games should derive from
# Should have the following methods:
#  setup()
#  playGame()
#  endGame()
# Includes the following member variables:
#  score - A number holding the current score
#  scoreKeeper - a ScoreKeeper object to record high scores
#  params - A GameParams object to hold relevant parameters

class Game:
  
  def __init__(self):
    self.score = 0
    self.scoreKeeper = ScoreKeeper()
    self.params = GameParams() # To be filled by user input
  
  def setup(self):
    raise NotImplementedError()
    
  def endGame(self):
    raise NotImplementedError()

  def playGame(self):
    raise NotImplementedError()

  def drawScore(self, window):
    if hasattr(self,'scoreText'):
      self.scoreText.string = str(self.score)
    else:
      self.scoreText = utils.drawText(window, size=25,
                         font=self.params.font, string=str(self.score))
    window.draw(self.scoreText)

