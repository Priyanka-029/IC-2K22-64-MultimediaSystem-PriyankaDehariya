Bloom Bouquet

A simple interactive 2D game built with Python 3 and Pygame. You are a florist with a basket. Customers place bouquet orders (for example 2 roses, 1 tulip and 3 daisies). Catch the right flowers as they fall, dodge weeds and bees, and finish each order before the timer runs out to make a beautiful bouquet.

1. How to Run

# 1. Install Python 3.8+ from https://www.python.org
# 2. Install Pygame
pip install pygame

# 3. Run the game from this folder
python flower.py

2. How to Play

1.Look at the Bouquet Order card at the top of the screen. It shows which flowers you need and how many.
2.Move the basket to catch the falling flowers on the order. Each correct flower gives +10, and you can see it appear in your basket.
3.When every flower on the order is collected, the bouquet is made: you get a bonus (50 + 2 points per second left) and a new, bigger order starts.
4.If the order timer runs out, you lose a life and get a new order.
5.The game ends when you lose all 3 lives.

Controls
Action	Control
Move basket	LEFT / RIGHT arrows, A / D, or mouse / touch (move the pointer)
Start game	ENTER, SPACE or click
Pause / resume	P or ESC
Mute / unmute	M
Play again (after game over)	R, ENTER, SPACE or click
Back to menu (after game over)	ESC

Project Stucture
BloomBouquetGame/
├── flower.py          ← Main game
├── requirements.txt
├── README.md      


