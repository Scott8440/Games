import shelve

class ScoreKeeper:
  
  def __init__(self):
    pass

  def setFile(self, fileName):
    self.scoreFile = fileName

  def checkScore(self, playerName, difficulty):
    scores = shelve.open(self.scoreFile, writeback=True)
    returnVal = 0
    if playerName in scores:
      if str(difficulty) in scores[playerName]:
        returnVal =  scores[playerName][str(difficulty)]
      else:
        scores[playerName][str(difficulty)] = 0
    scores.close()
    return returnVal


  def setScore(self, playerName, newScore, difficulty):
    scores = shelve.open(self.scoreFile, writeback=True)
    if playerName not in scores:
      scores[playerName] = {}
    scores[playerName][str(difficulty)] = newScore
    scores.close()
