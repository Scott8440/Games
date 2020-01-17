/*
  BUGS:
  1. Ball can get "stuck" on the bottom or top

*/

#include "Game.hpp"

#define WINDOW_WIDTH  800
#define WINDOW_HEIGHT 600

int main()
{
    srand(time(NULL));

    sf::RenderWindow window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "");

    // change the position of the window (relatively to the desktop)
    int x = 10; int y = 50;
    window.setPosition(sf::Vector2i(x, y));
    window.clear(sf::Color::Black);

    GameParameters params;
    Game game;
    do {
      params.gatherParameters(window);
      params.print();

      game.setup(window, params);

      game.runGame(window);
    } while(game.askReset(window));

}
