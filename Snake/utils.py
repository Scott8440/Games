from enum import Enum 
from sfml import sf
 
class Directions(Enum): 
  UP = 1 
  DOWN = 2 
  RIGHT = 3 
  LEFT = 4 

def centerWidth(window, text):
  return window.width/2 - text.local_bounds.width/2 

def centerHeight(window, text):
  return window.height/2 - text.local_bounds.height/2

def centerLocalHeight(heightLow, heightHigh, text):
  return (heightLow+heightHigh)/2 - text.local_bounds.height/2


def selectOptions(window, optionsStrings, selectValues, font):
    # creates a screen with options in vertical layout given by optionsStrings, and
    # returns the value from selectValues that is selected

    window.clear(sf.Color.BLACK)
    numOptions = len(optionsStrings)
    
    textObjects = []
    for string in optionsStrings:
      textObjects.append(sf.Text(string))

    for i in range(numOptions):
      text = textObjects[i]
      text.font = font
      text.character_size = 40
      text.color = sf.Color.WHITE
      areaLow = i*window.height//numOptions
      areaHight = areaLow + (window.height//numOptions)
      text.position = (centerWidth(window, text),
                      (centerLocalHeight(areaLow, areaHight, text)))

    optionChosen = False
    indexOfSelected = 0
    while(not optionChosen):
      window.clear(sf.Color.BLACK)
      
      mouseY = sf.Mouse.get_position(window)[1]



      for i in range(numOptions):
        color = None
        if i == indexOfSelected:
          color = sf.Color.GREEN
        else:
          color = sf.Color.WHITE
        textObjects[i].color = color 
  
      for text in textObjects:
        window.draw(text)
      
      for event in window.events:
        if type(event) is sf.CloseEvent:
          exit()

        if (type(event) is sf.MouseMoveEvent):
          indexOfSelected = int(mouseY//(window.height/numOptions))

        elif (type(event) is sf.MouseButtonEvent and event.pressed or
              type(event) is sf.KeyEvent and event.pressed and event.code == sf.Keyboard.RETURN):
          return selectValues[indexOfSelected]

        elif (type(event) is sf.KeyEvent and event.pressed):
          if (event.code == sf.Keyboard.DOWN or event.code == sf.Keyboard.RIGHT):
            indexOfSelected = (indexOfSelected + 1) % numOptions
          elif (event.code == sf.Keyboard.UP or event.code == sf.Keyboard.LEFT):
            indexOfSelected = (indexOfSelected - 1) % numOptions

      window.display()

def textInput(window, string, font, maxLength=None):
  window.clear(sf.Color.BLACK)
  text = sf.Text(string)
  text.font = font
  text.character_size = 40
  text.color = sf.Color.WHITE

  text.position = (centerWidth(window, text),
	          (centerHeight(window, text)))
  inputString = ""
  inputText = sf.Text(inputString)
  inputText.font = font
  inputText.character_size = 24
  inputText.color = sf.Color.GREEN
  inputText.position = (centerWidth(window, inputText),
                        text.position[1] + 30) 
  while True:
    window.clear(sf.Color.BLACK)
    for event in window.events:
       if type(event) is sf.CloseEvent:
         exit()
       if (type(event) is sf.TextEvent):
         if (ord(event.unicode) == 13 and len(inputString) > 1): #Enter
           return inputString

         elif (ord(event.unicode) == 8 and len(inputString) >= 1): # Backspace
           inputString = inputString[:-1]
           inputText = sf.Text(inputString)
           inputText.font = font
           inputText.character_size = 24
           inputText.color = sf.Color.GREEN
           inputText.position = (centerWidth(window, inputText),
                        text.position[1] + inputText.character_size + text.character_size) 

         elif (ord(event.unicode) < 127 and ord(event.unicode) >= 65):
           if (maxLength and len(inputString) == maxLength):
             continue
           inputString += event.unicode
           inputText = sf.Text(inputString)
           inputText.font = font
           inputText.character_size = 24
           inputText.color = sf.Color.GREEN
           inputText.position = (centerWidth(window, inputText),
                                 text.position[1] + inputText.character_size + text.character_size) 

    window.draw(text)
    window.draw(inputText)
    window.display()

  

def drawText(window, string="", size=30, font=None, position=(0,0), xposition=None, yposition=None, color=sf.Color.WHITE):
  text = sf.Text(string)
  text.character_size = size
  text.font = font
  if position == "center":
    text.position = (centerWidth(window, text), centerHeight(window, text))
  else:
    text.position = position 
  if xposition is not None:
    text.position = (xposition, text.position[1])
  if yposition is not None:
    text.position = (text.position[0], yposition)
  
  text.color = color
  window.draw(text)
  return text

def makeText(window, string="", size=30, font=None, position=(0,0), color=sf.Color.WHITE):
  text = sf.Text(string)
  text.character_size = size
  text.font = font
  if position == "center":
    text.position = (centerWidth(window, text), centerHeight(window, text))
  else:
    text.position = position 
  text.color = color
  return text


