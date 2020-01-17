
#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <SFML/Audio.hpp>
#include <iostream>
#include <stdlib.h>

using namespace std;

class GameParameters {

friend class Game;

private:
  float leftSpeed;
  float rightSpeed;

  float pongSpeed;

  bool  computerRight;         //Is right paddle controlled by a computer?
  float computerError;
  float computerReactionTime;

  sf::Keyboard::Key leftUp;
  sf::Keyboard::Key leftDown;

  sf::Keyboard::Key rightUp;
  sf::Keyboard::Key rightDown;

  void
  openScreen(sf::RenderWindow &window, sf::Time &time, sf::Clock &clock);

  void
  askPlayers(sf::RenderWindow &window);

  void
  askSpeed(sf::RenderWindow &window);

  void
  askDifficulty(sf::RenderWindow &window);

public:
  GameParameters();

  void
  gatherParameters(sf::RenderWindow &window);

  void
  print();


};
