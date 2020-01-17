#include "GameParameters.hpp"


GameParameters::GameParameters() {

  this->leftSpeed  = 5.0;
  this->rightSpeed = 5.0;

  this->pongSpeed = 4.0;

  this->computerRight = false;         //Is right paddle controlled by a computer?
  this->computerError = 40;
  this->computerReactionTime = 1.5;

  this->leftUp   = sf::Keyboard::W;
  this->leftDown = sf::Keyboard::S;

  this->rightUp   = sf::Keyboard::Up;
  this->rightDown = sf::Keyboard::Down;

}

void
GameParameters::gatherParameters(sf::RenderWindow &window) {

  sf::Clock clock;
  sf::Time elapsed = clock.getElapsedTime();

  openScreen(window, elapsed, clock);

  askPlayers(window);
  if (computerRight) {
    askDifficulty(window);
  }

  askSpeed(window);

}

void
GameParameters::askPlayers(sf::RenderWindow &window) {

  window.clear(sf::Color::Black);
  sf::Font font;
  if (!font.loadFromFile("LemonMilk.otf"))
  {
    cerr << "Bad Font File";
  }

  sf::Text player1Text;
  sf::Text player2Text;

  player1Text.setFont(font);
  player1Text.setString("1 Player");
  player1Text.setCharacterSize(50);
  player1Text.setColor(sf::Color::White);
  float textWidth = player1Text.getLocalBounds().width;
  float textHeight = player1Text.getLocalBounds().height;
  float winWidth  = window.getSize().x;
  float winHeight = window.getSize().y;
  player1Text.setPosition((winWidth/4)-(textWidth/2), winHeight/2 - (textHeight / 2));

  player2Text.setFont(font);
  player2Text.setString("2 Player");
  player2Text.setCharacterSize(50);
  player2Text.setColor(sf::Color::White);
  textWidth = player2Text.getLocalBounds().width;
  textHeight = player2Text.getLocalBounds().height;
  player2Text.setPosition((winWidth*(3.0/4.0))-(textWidth/2), winHeight/2 - (textHeight / 2));

  window.draw(player1Text);
  window.draw(player2Text);
  window.display();
  sf::sleep(sf::milliseconds(400));

  while (window.isOpen())
  {

    window.clear(sf::Color::Black);
    player1Text.setColor(sf::Color::White);
    player2Text.setColor(sf::Color::White);


    sf::Event event;
    while (window.pollEvent(event)) {
      if (event.type == sf::Event::Closed) {
          window.close();
      }

      if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::Escape) {       // Close on 'ESC'
          window.close();
        }
      }
    }

    if (sf::Mouse::getPosition(window).x < winWidth/2) {
      player1Text.setColor(sf::Color::Green);
    }
    else {
      player2Text.setColor(sf::Color::Green);
    }

    if (sf::Mouse::isButtonPressed(sf::Mouse::Left))
    {
      if (sf::Mouse::getPosition(window).x < winWidth/2) {
        computerRight = true;
      }
      else {
        computerRight = false;
      }
      break;
    }
    window.draw(player1Text);
    window.draw(player2Text);
    window.display();
  }
}

void
GameParameters::askSpeed(sf::RenderWindow &window) {
  window.clear(sf::Color::Black);
  sf::Font font;
  if (!font.loadFromFile("LemonMilk.otf"))
  {
    cerr << "Bad Font File";
  }

  float winWidth  = window.getSize().x;
  float winHeight = window.getSize().y;

  sf::Text slowText;
  sf::Text midText;
  sf::Text fastText;

  slowText.setFont(font);
  slowText.setString("slow");
  slowText.setCharacterSize(50);
  slowText.setColor(sf::Color::White);
  float textWidth = slowText.getLocalBounds().width;
  float textHeight = slowText.getLocalBounds().height;
  slowText.setPosition((winWidth/2)-(textWidth/2), winHeight/3 - (textHeight*2));

  midText.setFont(font);
  midText.setString("normal");
  midText.setCharacterSize(50);
  midText.setColor(sf::Color::White);
  textWidth = midText.getLocalBounds().width;
  textHeight = midText.getLocalBounds().height;
  midText.setPosition((winWidth/2)-(textWidth/2), winHeight/2 - (textHeight / 2));

  fastText.setFont(font);
  fastText.setString("fast");
  fastText.setCharacterSize(50);
  fastText.setColor(sf::Color::White);
  textWidth = fastText.getLocalBounds().width;
  textHeight = fastText.getLocalBounds().height;
  fastText.setPosition((winWidth/2)-(textWidth/2), winHeight/(3.0/2.0) + (textHeight));

  window.draw(slowText);
  window.draw(midText);
  window.draw(fastText);
  window.display();
  sf::sleep(sf::milliseconds(400));

  while (window.isOpen())
  {

    window.clear(sf::Color::Black);

    slowText.setColor(sf::Color::White);
    midText.setColor(sf::Color::White);
    fastText.setColor(sf::Color::White);


    float mouseY = sf::Mouse::getPosition(window).y;


    sf::Event event;
    while (window.pollEvent(event)) {
      if (event.type == sf::Event::Closed) {
          window.close();
      }

      if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::Escape) {       // Close on 'ESC'
          window.close();
        }
      }
    }

    if (mouseY < winHeight / 3) {
      slowText.setColor(sf::Color::Green);
    } else if (mouseY < winHeight * (2.0/3.0)) {
      midText.setColor(sf::Color::Green);
    } else if (mouseY < winHeight * 1) {
      fastText.setColor(sf::Color::Green);
    }


    if (sf::Mouse::isButtonPressed(sf::Mouse::Left))
    {
      if (mouseY < winHeight/3) {
        pongSpeed = 3.5;
      }
      else if (mouseY < winHeight * (2.0/3.0)){
        pongSpeed = 4.5;
      }
      else if (mouseY < winHeight * 1) {
        pongSpeed = 5.5;
      }
      break;
    }
    window.draw(slowText);
    window.draw(midText);
    window.draw(fastText);
    window.display();
  }
}

void
GameParameters::askDifficulty(sf::RenderWindow &window) {
  window.clear(sf::Color::Black);
  sf::Font font;
  if (!font.loadFromFile("LemonMilk.otf"))
  {
    cerr << "Bad Font File";
  }

  float winWidth  = window.getSize().x;
  float winHeight = window.getSize().y;

  sf::Text slowText;
  sf::Text midText;
  sf::Text fastText;

  slowText.setFont(font);
  slowText.setString("Easy");
  slowText.setCharacterSize(50);
  slowText.setColor(sf::Color::White);
  float textWidth = slowText.getLocalBounds().width;
  float textHeight = slowText.getLocalBounds().height;
  slowText.setPosition((winWidth/2)-(textWidth/2), winHeight/3 - (textHeight*2));

  midText.setFont(font);
  midText.setString("Medium");
  midText.setCharacterSize(50);
  midText.setColor(sf::Color::White);
  textWidth = midText.getLocalBounds().width;
  textHeight = midText.getLocalBounds().height;
  midText.setPosition((winWidth/2)-(textWidth/2), winHeight/2 - (textHeight / 2));

  fastText.setFont(font);
  fastText.setString("Hard");
  fastText.setCharacterSize(50);
  fastText.setColor(sf::Color::White);
  textWidth = fastText.getLocalBounds().width;
  textHeight = fastText.getLocalBounds().height;
  fastText.setPosition((winWidth/2)-(textWidth/2), winHeight/(3.0/2.0) + (textHeight));

  window.draw(slowText);
  window.draw(midText);
  window.draw(fastText);
  window.display();
  sf::sleep(sf::milliseconds(400));

  while (window.isOpen())
  {

    window.clear(sf::Color::Black);

    slowText.setColor(sf::Color::White);
    midText.setColor(sf::Color::White);
    fastText.setColor(sf::Color::White);


    float mouseY = sf::Mouse::getPosition(window).y;


    sf::Event event;
    while (window.pollEvent(event)) {
      if (event.type == sf::Event::Closed) {
          window.close();
      }

      if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::Escape) {       // Close on 'ESC'
          window.close();
        }
      }
    }

    if (mouseY < winHeight / 3) {
      slowText.setColor(sf::Color::Green);
    } else if (mouseY < winHeight * (2.0/3.0)) {
      midText.setColor(sf::Color::Green);
    } else if (mouseY < winHeight * 1) {
      fastText.setColor(sf::Color::Green);
    }


    if (sf::Mouse::isButtonPressed(sf::Mouse::Left))
    {
      if (mouseY < winHeight/3) {
        rightSpeed = 2.0;
        computerReactionTime = 1.5;
        computerError = 45;
      }
      else if (mouseY < winHeight * (2.0/3.0)){
        rightSpeed = 3.5;
        computerReactionTime = 1.0;
        computerError = 40;
      }
      else if (mouseY < winHeight * 1) {
        rightSpeed = 4;
        computerReactionTime = .75;
        computerError = 30;
      }
      break;
    }
    window.draw(slowText);
    window.draw(midText);
    window.draw(fastText);
    window.display();
  }
}

void
GameParameters::openScreen(sf::RenderWindow &window, sf::Time &elapsed, sf::Clock &clock) {

  sf::Font font;
  if (!font.loadFromFile("LemonMilk.otf"))
  {
    cerr << "Bad Font File";
  }

  sf::Text welcomeText;
  welcomeText.setFont(font);
  welcomeText.setString("PONG");
  welcomeText.setCharacterSize(74);
  welcomeText.setColor(sf::Color::White);
  float textWidth = welcomeText.getLocalBounds().width;
  float textHeight = welcomeText.getLocalBounds().height;
  float winWidth  = window.getSize().x;
  float winHeight = window.getSize().y;
  welcomeText.setPosition((winWidth/2)-(textWidth/2), winHeight/2 - (textHeight / 2));

  while (window.isOpen() && elapsed.asSeconds() < 5)
  {

    if (sf::Mouse::isButtonPressed(sf::Mouse::Left)) {
      break;
    }

    elapsed = clock.getElapsedTime();
    window.clear(sf::Color::Black);


    window.draw(welcomeText);


    sf::Event event;
    while (window.pollEvent(event))
    {
      if (event.type == sf::Event::Closed) {
          window.close();
      }

      if (event.type == sf::Event::KeyPressed) {
        if (event.key.code == sf::Keyboard::Escape) {       // Close on 'ESC'
          window.close();
        }
      }
    }
    window.display();
  }
}

void
GameParameters::print() {
  cout << "Parameters: " << endl;
  cout << "  AI: " << computerRight << endl;
  cout << "  LEFT SPEED:  " << leftSpeed << endl;
  cout << "  RIGHT SPEED: " << rightSpeed << endl;
  cout << "  PONG SPEED:  " << pongSpeed << endl;
  if (computerRight) {
    cout << "  AI ERROR:    " << computerError << endl;
    cout << "  AI REACTION: " << computerReactionTime << endl;
  }

}
