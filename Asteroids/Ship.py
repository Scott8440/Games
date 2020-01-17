from sfml import sf
from Bullet import Bullet
import math
import time
import utils

class Ship:
  def __init__(self, position=(100,100)):
    
    self.size = 15 
    self.rotation = 90 #Angle from vertical out of 360
    self.position = position
    self.velocity = (0,0)
    self.rotateSpeed = 3
    self.acceleration = 0.1 
    
    self.shape = sf.ConvexShape()
    self.shape.point_count = 3
    self.shape.set_point(0, (0,5))
    self.shape.set_point(1, (-10, -15))
    self.shape.set_point(2, (10, -15))
    self.shape.outline_thickness = 2
    self.shape.outline_color = sf.Color.WHITE
    self.shape.fill_color = sf.Color.BLACK
    self.shape.origin = (0, -8.333)
    
    self.refreshTime = 0.3
    self.lastShotTime = time.time()
    self.wrapping = False
    self.boundary = None

    # Collision Stuff
    samplePoint = self.shape.get_point(0)
    origin = self.shape.origin
    self.boundingRadius = ((samplePoint[0]-origin[0])**2 + 
                           (samplePoint[1]-origin[1])**2)**0.5
  
  def setBoundary(self, boundary):
    self.boundary = boundary
  
  def setWrapping(self, wrapping):
    self.wrapping = bool(wrapping)
  
  def getCooldown(self):
    return self.refreshTime

  def setCooldown(self, cooldown):
    self.refreshTime = cooldown
 
  def setRotateSpeed(self, speed):
    self.rotateSpeed = speed
  
  def getRotateSpeed(self):
    return self.rotateSpeed

  def setAcceleration(self, acc):
    self.acceleration = acc
   
  def getAcceleration(self):
    return self.acceleration

  def draw(self, window):
    self.shape.position = self.position
    window.draw(self.shape)

  def turnRight(self):
    self.rotation = (self.rotation + self.rotateSpeed) % 360
    self.shape.rotate(self.rotateSpeed)
  
  def turnLeft(self):
    self.rotation = (self.rotation - self.rotateSpeed) % 360
    self.shape.rotate(-self.rotateSpeed)
  
  def moveForward(self):
    # if wrapping, check if we need to change the position of the ship to 
    # the other side of the screen
    if self.wrapping and self.boundary:
      xPos = self.position[0]
      yPos = self.position[1]
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
      self.position = (newX + self.velocity[0],
                       newY + self.velocity[1])
    else:
      self.position = utils.add2d(self.position, self.velocity)

  def accelerate(self):
    # Adjust the velocity vector based on current heading
    acceleration = (self.acceleration*math.cos(math.pi/180 * self.rotation), 
                    self.acceleration*math.sin(math.pi/180 * self.rotation))
    self.velocity = utils.add2d(self.velocity, acceleration)

  def shootBullet(self, speed=10, boundary=None):
    if (time.time() - self.lastShotTime) < self.refreshTime:
      return None
    
    velocity = (speed*math.cos(math.pi/180 * self.rotation),
                speed*math.sin(math.pi/180 * self.rotation))

    bullet = Bullet(velocity, self.getTipPosition(), boundary=boundary)
    self.lastShotTime = time.time() 
    return bullet
   
  def getTipPosition(self):
    return self.getPointPosition(0) 
  
  def getPointPosition(self, index):
    return self.shape.transform.transform_point(self.shape.get_point(index))
  
  def circleTriangleCollision(self, circle):
    
    radius = circle.radius
    cX = circle.position[0] + radius # Add radius because position defines top-left corner
    cY = circle.position[1] + radius
    origin = self.shape.position

    # bound triangle in a circle to do easy filtering
    distanceFromOrigin = utils.distance2d(origin, (cX, cY))
    if distanceFromOrigin > (radius+self.boundingRadius):
      return False

    triangle = [self.getPointPosition(0), self.getPointPosition(1), self.getPointPosition(2)]
    return utils.circleTriangleCollision((cX, cY), radius, triangle)
