# Cource project: Alien shooter
The assignment was to implement a alien shooter game to PYNQ led board. 

## Led board
The first task was to make the leds work in the board. This was done by takign the led memory addresses and setting up the flow of the led channels. There are few methods to light up the leds

## Game logic
- The game boots up with a start screen
- The game can be restarted at any time
- The idea is to destroy the alien as many time as possible. The alien gets closer to the ship and it speeds up every 5 destroyed aliens.
- The points are shown after game is over
- Assembler led blinker is implemented to one of the buttons
