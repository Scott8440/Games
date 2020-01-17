//Game.hpp

/*
  TODO
    AI:
      > Make paddle move towards center after a point

    Pong:
      > Overload checkCollision() to take less arguments for imaginary ball
*/

#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <SFML/Audio.hpp>
#include "Pong.hpp"
#include "Paddle.hpp"
#include "GameParameters.hpp"
#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <time.h>
#include <string>

#define PONG_SIZE      12
#define PADDLE_HEIGHT  50
#define PADDLE_WIDTH   10

#define SCORE_TEXT_SIZE 24
#define END_GAME_TEXT_SIZE 48

#define AI_PADDLE_BOUND 5

#define BACKGROUND_COLOR sf::Color::Black

#define WIN_SCORE 10

#define START_ANGLE_MAX 60

#define HIGH_ANGLE 15
#define MID_ANGLE 45



using namespace std;


class Game {
private:

  int leftScore;
  int rightScore;

  Pong   ball;                  // Pong objects
  Pong   invisibleBall;
  float  invBallLoc;

  Paddle left;
  Paddle right;

  sf::Music music;              // Music Data -> This could go in parameters
  string musicFile;
  sf::SoundBuffer buffer;
  sf::Sound sound;

  sf::Clock clock;              // Time data
  sf::Time elapsed;

  sf::Text rightText;          // Text data
  sf::Text leftText;
  sf::Font font;
  string fontFile;

  GameParameters params;       // Other data

  void
  leftPoint() {
    ++leftScore;
    leftText.setString(to_string(leftScore));
  }

  void
  rightPoint() {
    ++rightScore;
    rightText.setString(to_string(rightScore));
  }

  void
  reset(sf::RenderWindow &window);

  void
  movePaddles(Paddle &left, Paddle &right, sf::RenderWindow &window);

  void
  drawScreen(sf::RenderWindow &window);

  void
  endGameVictory(sf::RenderWindow &window);

  void
  endGameDefeat(sf::RenderWindow &window);

  void
  handleInput(sf::Event event, sf::RenderWindow &window);

  int
  checkCollision(Paddle& left, Paddle &right, Pong &ball,
                 sf::RenderWindow &window, bool &bounced, bool &bouncedRight, bool wallsOnly);

  void
  moveInvisible(sf::RenderWindow &window);

  void
  moveToCenter(sf::RenderWindow &window, Paddle &paddle);


public:

  Game() {}

 ~Game() {};

  void
  setup(sf::RenderWindow &window, GameParameters &params);

  void
  runGame(sf::RenderWindow &window);

  bool
  askReset(sf::RenderWindow &window);


};
