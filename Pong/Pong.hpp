/*

*/

#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <SFML/Audio.hpp>
#include "Paddle.hpp"
#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <time.h>
#include <string>

#define PI 3.14159265                           // For angle conversions

using namespace std;



class Pong : public sf::RectangleShape {
private:
  float velocity;
  int direction;
  int   size;



public:
  Pong() =default;
  Pong(int size, float x_start, float y_start, float vel);   //Initialize

  void bounceVert();          // Switches y-velocity
  void bounceHoriz();         // Switches x-velocity

  // Move ball based on velocity, checkcollision, and bounce if necessary
  void movePong(Paddle &left, Paddle &right, sf::RenderWindow &window);

  void setVelocity(float vel) {
    velocity = vel;
  }

  float getVelocity() { return velocity; }

  void setDirection(float dir) {
    direction = ((int) dir) % 360;
  }

  float getDirection() { return direction; }

};
