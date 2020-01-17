

#-----------------------------------------------------------
# Macro definitions
CXXFLAGS = g++ -g -Wall -O1 -std=c++14
OBJ = main.o Game.o Pong.o Paddle.o GameParameters.o
SFML-LIBS = -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio
TARGET = pong
#-----------------------------------------------------------
# Rules
all: $(TARGET)

pong: $(OBJ)
	$(CXXFLAGS) -o $(TARGET) $(OBJ) $(SFML-LIBS)

%.o: %.cpp
	$(CXXFLAGS) -c $< -o $@

%.o: %.hpp
	$(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET) $(CLASSES)
#-----------------------------------------------------------
# Dependencies
# main.o: main.cpp MyCircle.hpp Body.hpp
# MyCircle.o: MyCircle.cpp MyCircle.hpp
# Body.o: Body.hpp MyCircle.hpp
