
#include "Paddle.hpp"


Paddle::Paddle(int height, int width, float speed, float x_loc) {
  this->moveSpeed = speed;
  this->height = height;
  this->width = width;
  this->setSize(sf::Vector2f(width, height));
  this->setFillColor(sf::Color::White);
  this->setPosition(x_loc, 400);
}

void
Paddle::movePaddle(Direction dir) {
  if (dir == Up) {
    move(0, -1 * moveSpeed);
  }
  else {
    move(0, moveSpeed);
  }
}
