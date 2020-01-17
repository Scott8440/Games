


class AutoPaddle : public Paddle {
public:
  AutoPaddle() : Paddle() {}
  AutoPaddle(int height, int width, float speed, float x_loc) : Paddle(height, width, speed, x_loc) {}

  void movePaddle(float location);

}
