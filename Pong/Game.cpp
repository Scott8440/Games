

#include "Game.hpp"


void
Game::setup(sf::RenderWindow &window, GameParameters &parameters) {

  params = parameters;
  // Data Setup
    rightScore = 0;
    leftScore = 0;


  // Pong Setup =========================================================
  ball = Pong(PONG_SIZE, window.getSize().x / 2, window.getSize().y / 2, params.pongSpeed);
  left = Paddle(PADDLE_HEIGHT, PADDLE_WIDTH, params.leftSpeed, 0);
  right = Paddle(PADDLE_HEIGHT, PADDLE_WIDTH, params.rightSpeed, window.getSize().x - 10);


  // Audio Setup =============================================================

  musicFile = "DNBTTLoop3.wav";
  if (!music.openFromFile(musicFile)) {
    cerr << "Could not open music file: " << musicFile << endl;
  }
  else {
    music.setLoop(true);
    //music.play();
  }

  if (!buffer.loadFromFile("bounce.wav")) {
        cerr << "Couldn't Load Sound File" << endl;
  }

  sound.setBuffer(buffer);


  // Clock Setup =============================================================

  sf::Clock clock;
  elapsed = clock.getElapsedTime();

  // End Clock Setup =========================================================


  // Text Setup ==============================================================
  fontFile = "LemonMilk.otf";
  if (!font.loadFromFile(fontFile))
  {
    cerr << "Bad Font File";
  }

  sf::Vector2u winSize = window.getSize();

  // Main Circle Health
  rightText.setFont(font);
  rightText.setString(to_string(rightScore));
  rightText.setCharacterSize(SCORE_TEXT_SIZE);
  rightText.setColor(sf::Color::White);
  rightText.setPosition(winSize.x-30, 0);

  // Player Health
  leftText.setFont(font);
  leftText.setString(to_string(leftScore));
  leftText.setCharacterSize(SCORE_TEXT_SIZE);
  leftText.setColor(sf::Color::White);
  leftText.setPosition(15, 0);
}

void
Game::movePaddles(Paddle &left, Paddle &right, sf::RenderWindow &window) {
  // Handle left Paddle Movements
  if (sf::Keyboard::isKeyPressed(params.leftUp) &&
      left.getPosition().y > 0)
  {
    left.movePaddle(Up);
  }
  if (sf::Keyboard::isKeyPressed(params.leftDown) &&
      left.getPosition().y + left.getSize().y < window.getSize().y) 
  {
    left.movePaddle(Down);
  }

  // Handle Right Paddle Movements
  if (!params.computerRight) {
    if (sf::Keyboard::isKeyPressed(params.rightUp) &&
        right.getPosition().y > 0)
    {
      right.movePaddle(Up);
    }
    if (sf::Keyboard::isKeyPressed(params.rightDown) &&
        right.getPosition().y + right.getSize().y < window.getSize().y)
    {
      right.movePaddle(Down);
    }
  }
  else {
    // Automatically move right pong paddle
    sf::Vector2f rightLoc = right.getPosition();
    sf::Vector2f rightSize = right.getSize();

    float rightCenter = rightLoc.y + rightSize.y/2;

    elapsed = clock.getElapsedTime();
    if (elapsed.asSeconds() > params.computerReactionTime) {
      if (rightCenter > invBallLoc + AI_PADDLE_BOUND &&
          right.getPosition().y > 0)
      {
        right.movePaddle(Up);
      }
      else if (rightCenter <= invBallLoc - AI_PADDLE_BOUND &&
               right.getPosition().y + right.getSize().y < window.getSize().y)
      {
        right.movePaddle(Down);
      }
    }
  }
}

void
Game::runGame(sf::RenderWindow &window) {

  sf::RectangleShape dummy;
  sf::RectangleShape dummy2;

  invisibleBall = Pong(PONG_SIZE, ball.getPosition().x, ball.getPosition().y, ball.getVelocity());
  invBallLoc = window.getSize().y/2;      //End Location of Invisible Ball
  moveInvisible(window);
  bool bouncedRight = false;

  while (window.isOpen())
  {
      sf::Event event;
      while (window.pollEvent(event))
      {
          handleInput(event, window);
      }
      movePaddles(left, right, window);

      ball.movePong(left, right, window);

      bool bouncedLeft  = false;
      int score = checkCollision(left, right, ball, window, bouncedLeft, bouncedRight, false);

      if (bouncedLeft && params.computerRight) {                  // bounced off left, create invisibleBall and calculate automatic
        moveInvisible(window);
        // dummy.setPosition(invisibleBall.getPosition().x, invisibleBall.getPosition().y);
        // dummy.setSize(sf::Vector2f(12, 12));
        // dummy.setOutlineColor(sf::Color::Red);
        // dummy.setOutlineThickness(5);
        // dummy2.setPosition(invisibleBall.getPosition().x, invBallLoc);
        // dummy2.setSize(sf::Vector2f(12, 12));
        // dummy2.setOutlineColor(sf::Color::Yellow);
        // dummy2.setOutlineThickness(5);
        clock.restart();
        bouncedRight = false;
        right.setSpeed(params.rightSpeed);
      }
      if (bouncedRight && params.computerRight && params.computerReactionTime < 1) {
        //moveToCenter(window, right);
        invBallLoc = window.getSize().y/2;
        right.setSpeed(params.rightSpeed/2);

      }

      if (score == 1) {
        rightPoint();
        window.draw(rightText);
        reset(window);
        bouncedRight = false;
        moveInvisible(window);

      }
      else if (score == 0) {
        leftPoint();
        window.draw(leftText);
        reset(window);
        bouncedRight = false;
        moveInvisible(window);

      }

      if (leftScore == WIN_SCORE) {
        endGameVictory(window);
        break;
      }
      else if (rightScore == WIN_SCORE) {
        endGameDefeat(window);
        break;
      }
      else {
        window.draw(dummy);
        window.draw(dummy2);
        drawScreen(window);
      }
  }
  music.stop();
}


void
Game::drawScreen(sf::RenderWindow &window) {
  window.clear(BACKGROUND_COLOR);
  window.draw(leftText);
  window.draw(rightText);
  window.draw(ball);
  window.draw(left);
  window.draw(right);
  window.display();
  sf::sleep(sf::milliseconds(10));
}

void
Game::handleInput(sf::Event event, sf::RenderWindow &window) {

  if (event.type == sf::Event::Closed) {
      window.close();
  }

  if (event.type == sf::Event::KeyPressed) {
    if (event.key.code == sf::Keyboard::Escape) {       // Close on 'ESC'
      window.close();
    }
  }
}

void
Game::reset(sf::RenderWindow &window) {
  window.clear(BACKGROUND_COLOR);
  ball.setPosition(sf::Vector2f(window.getSize().x/2, window.getSize().y/2));
  ball.setVelocity(params.pongSpeed);
  float dir = rand()%(START_ANGLE_MAX-(-START_ANGLE_MAX) + 1) + (-START_ANGLE_MAX);
  float r = (float) rand() / RAND_MAX;
  if (r < 0.5) { dir += 180; }   // 50% chance of shooting left
  ball.setDirection(dir);
  drawScreen(window);
  sf::Time t = clock.getElapsedTime();
  while (clock.getElapsedTime().asSeconds() - t.asSeconds() < 1) {
    sf::Event event;
    while (window.pollEvent(event))
    {
        handleInput(event, window);
    }
    movePaddles(left, right, window);
    drawScreen(window);
  }
}

void
Game::endGameVictory(sf::RenderWindow &window) {
  window.clear(BACKGROUND_COLOR);
  sf::Text text;
  text.setFont(font);
  text.setCharacterSize(END_GAME_TEXT_SIZE);
  text.setString("You Won!");
  text.setColor(sf::Color::White);
  int width = text.getLocalBounds().width;
  int winWidth = window.getSize().x;
  int winHeight = window.getSize().y;
  text.setPosition(winWidth / 2 - width/2, winHeight / 2);
  window.draw(text);
  window.display();
  sf::sleep(sf::milliseconds(3000));
  askReset(window);
}

void
Game::endGameDefeat(sf::RenderWindow &window) {
  window.clear(BACKGROUND_COLOR);
  sf::Text text;
  text.setFont(font);
  text.setCharacterSize(END_GAME_TEXT_SIZE);
  text.setString("You Lost");
  text.setColor(sf::Color::White);
  int width = text.getLocalBounds().width;
  int winWidth = window.getSize().x;
  int winHeight = window.getSize().y;
  text.setPosition(winWidth / 2 - width/2, winHeight / 2);
  window.draw(text);
  window.display();
  sf::sleep(sf::milliseconds(3000));
  askReset(window);
}

bool
Game::askReset(sf::RenderWindow &window) {
  window.clear(sf::Color::Black);
  sf::Font font;
  if (!font.loadFromFile("LemonMilk.otf"))
  {
    cerr << "Bad Font File";
  }

  sf::Text yesText;
  sf::Text noText;
  sf::Text title;

  title.setFont(font);
  title.setString("Play Again?");
  title.setCharacterSize(50);
  title.setColor(sf::Color::White);
  float textWidth = title.getLocalBounds().width;
  float textHeight = title.getLocalBounds().height;
  float winWidth  = window.getSize().x;
  float winHeight = window.getSize().y;
  title.setPosition((winWidth/2)-(textWidth/2), winHeight/4 - (textHeight / 2));

  yesText.setFont(font);
  yesText.setString("yes");
  yesText.setCharacterSize(50);
  yesText.setColor(sf::Color::White);
  textWidth = yesText.getLocalBounds().width;
  textHeight = yesText.getLocalBounds().height;
  yesText.setPosition((winWidth/4)-(textWidth/2), winHeight/2 - (textHeight / 2));

  noText.setFont(font);
  noText.setString("no");
  noText.setCharacterSize(50);
  noText.setColor(sf::Color::White);
  textWidth = noText.getLocalBounds().width;
  textHeight = noText.getLocalBounds().height;
  noText.setPosition((winWidth*(3.0/4.0))-(textWidth/2), winHeight/2 - (textHeight / 2));

  window.draw(yesText);
  window.draw(noText);
  window.draw(title);
  window.display();
  sf::sleep(sf::milliseconds(400));

  while (window.isOpen())
  {

    window.clear(sf::Color::Black);
    yesText.setColor(sf::Color::White);
    noText.setColor(sf::Color::White);


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
      yesText.setColor(sf::Color::Green);
    }
    else {
      noText.setColor(sf::Color::Green);
    }

    if (sf::Mouse::isButtonPressed(sf::Mouse::Left))
    {
      if (sf::Mouse::getPosition(window).x < winWidth/2) {
        return true;
      }
      else {
        return false;
      }
      break;
    }
    window.draw(yesText);
    window.draw(noText);
    window.draw(title);
    window.display();
  }
  return false;
}

int
Game::checkCollision(Paddle &left, Paddle &right, Pong &ball,
                     sf::RenderWindow &window, bool &bounced, bool &bouncedRight, bool wallsOnly) {
  sf::Vector2u winSize   = window.getSize();
  sf::Vector2f pongLoc   = ball.getPosition();
  sf::Vector2f pongSize  = ball.getSize();
  sf::Vector2f leftLoc   = left.getPosition();
  sf::Vector2f leftSize  = left.getSize();
  sf::Vector2f rightLoc  = right.getPosition();
  sf::Vector2f rightSize = right.getSize();

  float leftTop    = leftLoc.y;
  float leftBottom = leftLoc.y + leftSize.y;

  float rightTop    = rightLoc.y;
  float rightBottom = rightLoc.y + rightSize.y;

  float pongTop    = pongLoc.y;
  float pongCenter = pongLoc.y + pongSize.y/2;
  float pongBottom = pongLoc.y + pongSize.y;

  //Check for collision with borders
  if (pongLoc.x <= 0) {
    return 1;             //point for right
  }
  else if (pongLoc.x + pongSize.x >= winSize.x) {
    return 0;             //point for left
  }
  if (pongLoc.y <= 0 &&
      ball.getVelocity() * sin(ball.getDirection()*3.1416/180) < 0) {
    ball.bounceVert();         //Bounce Down
  }
  else if (pongLoc.y + pongSize.x >= winSize.y &&
           ball.getVelocity() * sin(ball.getDirection()*3.1416/180) > 0) {
    ball.bounceVert();         //Bounce Up
  }
  if (wallsOnly == true) { return -1; }
  //Check for collision with Left Paddle
  if ((pongLoc.x <= leftLoc.x + leftSize.x) &&
      (pongBottom >= leftTop && pongTop <= leftBottom))
  {
    sound.play();
    bounced = true;
    float randBounce = 10 * ((((float) rand()) / (float) RAND_MAX)) + -5;
    if        (pongCenter < leftTop + (1.0/8.0) * leftSize.y) {   // 15 deg up
      ball.setDirection(360-HIGH_ANGLE + randBounce);
      if (ball.getVelocity() == params.pongSpeed) {
        ball.setVelocity(ball.getVelocity()*1.5);
      }
    }
    else if (pongCenter < leftTop + (3.0/8.0) * leftSize.y) {   // 45 deg up
      ball.setDirection(360-HIGH_ANGLE + randBounce);
      ball.setVelocity(params.pongSpeed);
    }
    else if (pongCenter < leftTop + (5.0/8.0) * leftSize.y) {   // normal reflection
      ball.bounceHoriz();
      ball.setVelocity(params.pongSpeed);

    }
    else if (pongCenter < leftTop + (5.0/8.0) * leftSize.y) {  // 45 deg down
      ball.setDirection(HIGH_ANGLE + randBounce);
      ball.setVelocity(params.pongSpeed);
    }
    else {                                                      // 15 deg down
      ball.setDirection(MID_ANGLE + randBounce);
      if (ball.getVelocity() == params.pongSpeed) {
        ball.setVelocity(ball.getVelocity()*1.5);
      }
    }
  }
  else if ((pongLoc.x +pongSize.x >= rightLoc.x) &&            //same horizontal position
          (pongBottom >= rightTop && pongTop <= rightBottom))
  {
    bouncedRight = true;
    sound.play();
    float randBounce = 10 * ((((float) rand()) / (float) RAND_MAX)) + -5;
    if        (pongCenter < rightTop + (1.0/8.0) * rightSize.y) {   // 15 deg up
      ball.setDirection(MID_ANGLE + 180 + randBounce);
      if (ball.getVelocity() == params.pongSpeed) {
        ball.setVelocity(ball.getVelocity()*1.5);
      }
    }
    else if (pongCenter < rightTop + (3.0/8.0) * rightSize.y) {   // 45 deg up
      ball.setDirection(HIGH_ANGLE + 180 + randBounce);
      ball.setVelocity(params.pongSpeed);
    }
    else if (pongCenter < rightTop + (5.0/8.0) * rightSize.y) {   // normal reflection
      ball.bounceHoriz();
      ball.setVelocity(params.pongSpeed);

    }
    else if (pongCenter < rightTop + (5.0/8.0) * rightSize.y) {  // 45 deg down
      ball.setDirection(360-HIGH_ANGLE + 180 + randBounce);
      ball.setVelocity(params.pongSpeed);
    }
    else {                                                      // 15 deg down
      ball.setDirection(360-MID_ANGLE + 180 + randBounce);
      if (ball.getVelocity() == params.pongSpeed) {
        ball.setVelocity(ball.getVelocity()*1.5);
      }
    }
  }
  return -1;
}

void
Game::moveInvisible(sf::RenderWindow &window) {
  bool bounced;
  bool bouncedRight;
  invisibleBall.setPosition(ball.getPosition().x, ball.getPosition().y);
  invisibleBall.setVelocity(ball.getVelocity());
  invisibleBall.setDirection(ball.getDirection());

  if (invisibleBall.getVelocity() * cos(invisibleBall.getDirection()*3.1416/180) <= 0) { return; }

  while (invisibleBall.getPosition().x <= window.getSize().x-(left).getSize().x) {
    invisibleBall.movePong(left, right, window);
    checkCollision(left, right, invisibleBall, window, bounced, bouncedRight, true);
  }
  float randError = (params.computerError*2) * ((((float) rand()) / (float) RAND_MAX)) - params.computerError;
  invBallLoc = invisibleBall.getPosition().y + randError;
}

void
Game::moveToCenter(sf::RenderWindow &window, Paddle &paddle) {
  cout << "Move to center " << endl;
  float center = window.getSize().y / 2;
  float paddleLoc = paddle.getPosition().y;
  float paddleSize = paddle.getSize().y;
  cout << "Paddle: " << paddleLoc << endl;

  float paddleCenter = paddleLoc + paddleSize/2;

  if (paddleCenter > center) {
    paddle.movePaddle(Up);
  }
  else if (paddleCenter < center) {
    paddle.movePaddle(Down);
  }
}
