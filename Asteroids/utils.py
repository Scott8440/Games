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
     
         elif (ord(event.unicode) < 127 and ord(event.unicode) >= 65): #regular character
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
  text.color = color
  if position == "center":
    text.position = (centerWidth(window, text), centerHeight(window, text))
  else:
    text.position = position 
  if xposition is not None:
    text.position = (xposition, text.position[1])
  if yposition is not None:
    text.position = (text.position[0], yposition)
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

def project2d(a, b):
  # Projects a onto b
  #abdot = (a[0]*b[0])+(a[1]*b[1])
  abdot = a[0]*b[0]
  blensq = (b[0]*b[0])+(b[1]*b[1])
  temp = abdot/blensq
  c = (b[0]*temp,b[1]*temp)
  return c

def length2d(a):
  return (a[0]**2 + a[1]**2)**0.5

def add2d(a,b):
  x = a[0] + b[0]
  y = a[1] + b[1]
  return (x,y)

def subtract2d(a,b):
  x = a[0] - b[0]
  y = a[1] - b[1]
  return (x,y)

def distance2d(a,b):
  return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

def circleTriangleCollision(circle, radius, triangle):
  # circle is a point defining the center of the circle
  # triangle is a list of 3 vertices

  # TEST 1: Vertex within circle
  centerX = circle[0]
  centerY = circle[1]
  
  v1x = triangle[0][0]
  v1y = triangle[0][1]  
  v2x = triangle[1][0]
  v2y = triangle[1][1]  
  v3x = triangle[2][0]
  v3y = triangle[2][1]  

  c1x = centerX - v1x
  c1y = centerY - v1y

  radiusSqr = radius*radius
  c1sqr = c1x*c1x + c1y*c1y - radiusSqr

  if c1sqr <= 0:
    return True

  c2x = centerX - v2x
  c2y = centerY - v2y
  c2sqr = c2x*c2x + c2y*c2y - radiusSqr

  if c2sqr <= 0:
    return True

  c3x = centerX - v3x
  c3y = centerY - v3y
  c3sqr = c3x*c3x + c3y*c3y - radiusSqr

  if c3sqr <= 0:
    return True

  # TEST 2: Circle centre within triangle
  # Calculate edges
  e1x = v2x - v1x
  e1y = v2y - v1y
  e2x = v3x - v2x
  e2y = v3y - v2y
  e3x = v1x - v3x
  e3y = v1y - v3y
  #if signed((e1y*c1x - e1x*c1y) | (e2y*c2x - e2x*c2y) | (e3y*c3x - e3x*c3y)) >= 0
  #  return true
  # TEST 3: Circle intersects edge

  k = c1x*e1x + c1y*e1y
  if k > 0:
    length = e1x*e1x + e1y*e1y     # squared length
    if k < length:
      if c1sqr * length <= k*k:
        return True

  # Second edge
  k = c2x*e2x + c2y*e2y
  if k > 0:
    length = e2x*e2x + e2y*e2y
    if k < length:
      if c2sqr * length <= k*k:
        return True

  # Third edge
  k = c3x*e3x + c3y*e3y
  if k > 0:
    length = e3x*e3x + e3y*e3y
    if k < length:
      if c3sqr * length <= k*k:
        return True
  return False
