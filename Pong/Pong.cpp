

#include "Pong.hpp"


Pong::Pong(int size, float x_start, float y_start, float vel) {
  srand(time(NULL));

  this->size = size;
  this->setPosition(x_start, y_start);
  this->setSize(sf::Vector2f(size, size));
  float dir = rand()%(60-(-60) + 1) + (-60);              //rand between -60 and 60
  if (((float)rand()/(RAND_MAX)) < 0.5) { dir += 180; }   // 50% chance of shooting left

  this->velocity = vel;
  this->direction = dir;
  this->setFillColor(sf::Color::White);
}

void
Pong::movePong(Paddle &left, Paddle &right, sf::RenderWindow &window) {  // Move based on Velocity
  //int ret = checkCollision(left, right, window);
  float x_vel = velocity * cos(getDirection()*PI/180);
  float y_vel = velocity * sin(getDirection()*PI/180);
  move(x_vel, y_vel);
  //return ret;
}

void
Pong::bounceVert() {
  // Switch y direction
  direction = (getDirection() * -1);
  if (direction > 360) { direction -= 360; }
  if (direction < 0) { direction += 360; }
}

void
Pong::bounceHoriz() {
  // Switch x direction
  direction = (180 - getDirection());
  if (direction > 360) { direction -= 360; }
  else if (direction < 0) { direction += 360; }
}
