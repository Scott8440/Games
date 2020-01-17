from sfml import sf
import utils
import random


class Asteroid:

  def __init__(self, size, position, velocity, boundary=None, wrapping=False):
    self.size = size
    self.sizeMultiplier = 5
    self.velocity = velocity
    self.shape = sf.CircleShape(size*self.sizeMultiplier)
    self.shape.position = position
    self.shape.outline_thickness = 1
    self.shape.outline_color = sf.Color.WHITE
    self.shape.fill_color = sf.Color.BLACK
    self.boundary = boundary
    self.wrapping = wrapping

  def draw(self, window):
    window.draw(self.shape)

  def setWrapping(self, wrapping):
    self.wrapping = bool(wrapping)

  def setBoundary(self, boundary):
    self.boundary = boundary

  def getShape(self):
    return self.shape

  def move(self):
    if self.wrapping and self.boundary:
      xPos = self.shape.position[0]
      yPos = self.shape.position[1]
      newX = xPos
      newY = yPos

      if (yPos < -self.size):
        newY = self.boundary[1] + self.size
      elif (yPos > self.boundary[1] + self.size):
        newY = -self.size
      if (xPos < -self.size):
        newX = self.boundary[0] + self.size
      elif (xPos > self.boundary[0] + self.size):
        newX = -self.size
      self.shape.position = (newX + self.velocity[0],
                             newY + self.velocity[1])
    else:
      newPosition = (self.shape.position[0] + self.velocity[0],
                     self.shape.position[1] + self.velocity[1])
      self.shape.position = newPosition

  def breakAsteroid(self):
    # returns array of multiple new smaller asteroids 
    # at random velocities at same position

    if self.size == 1:
      return None
    else: 
      numToCreate = self.size - 1
      newSize = self.size - 1

      asteroids = []
      positionRandomizer = 3
      velocityRandomizer = 2
      for i in range(numToCreate):
        # make the position slightly different so they don't all start on top of each other
        position = (self.shape.position[0] + random.uniform(-1,1)*positionRandomizer,
                    self.shape.position[1] + random.uniform(-1,1)*positionRandomizer)
        velocity = (random.uniform(-1,1)*velocityRandomizer,
                    random.uniform(-1,1)*velocityRandomizer)
        asteroids.append(Asteroid(newSize, position, velocity, wrapping=self.wrapping, boundary = self.boundary))
      return asteroids

  def didCollide(self, shape):
    radius = self.shape.radius
    center = (self.shape.position[0] + radius,
              self.shape.position[1] + radius)
    return (utils.distance2d(center, shape.getPosition()) <= radius)

  def shouldDelete(self):
    # No reason to delete an asteroid as it will be removed
    # when it is destroyed or split
    return False
