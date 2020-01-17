/*
  TODO:
    > Make a derived class AutoPaddle that moves automatically
      > Make movePaddle() virtual ?
*/

#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <SFML/Audio.hpp>
#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <time.h>
#include <string>

using namespace std;

enum Direction {Up, Down };

class Paddle : public sf::RectangleShape {
private:
  int height;
  int width;
  float moveSpeed;

public:
  Paddle() = default;
  Paddle(int height, int width, float speed, float x_loc);

  void movePaddle(Direction dir);

  void setSpeed(float speed) { moveSpeed = speed; }


};
