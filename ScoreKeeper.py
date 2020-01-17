import shelve

class ScoreKeeper:
  
  def __init__(self):
    pass

  def setFile(self, fileName):
    self.scoreFile = fileName

  def checkScore(self, playerName):
    
    scores = shelve.open(self.scoreFile)
    if playerName in scores:
      return scores[playerName]
    else:
      return 0

  def setScore(self, playerName, newScore):
    
    scores = shelve.open(self.scoreFile)
    scores[playerName] = newScore
