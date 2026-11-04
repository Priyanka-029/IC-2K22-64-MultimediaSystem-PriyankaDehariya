# Bloom Bouquet

A simple interactive 2D game built with **Python 3** and **Pygame**.
You are a florist with a basket. Customers place **bouquet orders** (for example 2 roses, 1 tulip and 3 daisies).
Catch the right flowers as they fall, dodge weeds and bees, and finish each order before the timer runs out
to make a beautiful bouquet.

> Student: *Your Name Here*  |  Course / Roll No: *fill in*

---

## 1. How to Run

```bash
# 1. Install Python 3.8+ from https://www.python.org
# 2. Install Pygame
pip install pygame

# 3. Run the game from this folder
python bloom_bouquet.py
```

No image or sound files are needed. All sprites, backgrounds and audio are generated in code,
so the whole project is a single file (`bloom_bouquet.py`).

---

## 2. How to Play

1. Look at the **Bouquet Order** card at the top of the screen. It shows which flowers you need and how many.
2. Move the basket to catch the falling flowers on the order. Each correct flower gives **+10**, and you can see it appear in your basket.
3. When every flower on the order is collected, the bouquet is made: you get a **bonus** (50 + 2 points per second left) and a new, bigger order starts.
4. If the order timer runs out, you lose a life and get a new order.
5. The game ends when you lose all **3 lives**.

### Controls

| Action | Control |
|---|---|
| Move basket | `LEFT` / `RIGHT` arrows, `A` / `D`, **or** mouse / touch (move the pointer) |
| Start game | `ENTER`, `SPACE` or click |
| Pause / resume | `P` or `ESC` |
| Mute / unmute | `M` |
| Play again (after game over) | `R`, `ENTER`, `SPACE` or click |
| Back to menu (after game over) | `ESC` |

### Objects

| Object | Effect |
|---|---|
| Rose, Tulip, Sunflower, Daisy, Lavender | +10 if it is on your order and still needed; **-5** if it is not needed |
| Weed (spinning, spiky) | -1 life, -10 points |
| Bee (fast, zig-zags) | -1 life, -10 points |
| Wilted flower | -10 points and removes the last flower you collected |
| Dew drop | +8 seconds on the order timer |

---

## 3. Individual Customization: The Wind Gust Event

Every **15 seconds** a **Wind Gust** blows for **5 seconds**. It changes the game's appearance,
rules and behaviour at the same time:

- **Appearance:** petals and leaves fly across the screen, the clouds speed up, and a "WIND GUST" banner shows the direction.
- **Rules:** the gust pushes every falling flower, weed and bee sideways, so a flower you lined up may land somewhere else.
- **Behaviour:** the wind builds up, peaks and fades smoothly, so you have to predict where each object will land.

All wind settings, plus your name, title, colours and timer lengths, are in the `CONFIG` dictionary at the top of
`bloom_bouquet.py`:

```python
CONFIG = {
    "title": "BLOOM BOUQUET",
    "student_name": "Your Name Here",
    "sky_top": (120, 195, 245),
    "sky_bottom": (215, 240, 255),
    "grass_color": (92, 170, 80),
    "ribbon_color": (235, 70, 130),
    "start_lives": 3,
    "wind_every": 15.0,
    "wind_duration": 5.0,
    "wind_strength": 150.0,
    "order_time_base": 18.0,
    "order_time_per_flower": 6.0,
}
```

> If your instructor assigned you a specific customization, change these values, or edit the
> `FLOWERS` table, the scoring in `on_catch()` or the wind code in `update()` to match it.

---

## 4. Requirements Checklist

| Requirement | Where it is implemented |
|---|---|
| Start screen and instructions | `draw_menu()` shows the title, flower and hazard legend with sprites, and the controls |
| Gameplay screen, score, timer, lives | `draw_hud()` and `draw_order_card()` show score, best score, level, play time, hearts and the order timer bar |
| Player controls (keyboard + mouse/touch) | `update()` and `handle_event()` |
| Animation / continuous updates | Falling, swaying and spinning objects, flapping bee wings, moving clouds, wind petals, particles, floating text, screen shake, bouquet celebration |
| Collision detection | `Rect.colliderect()` between the basket's catch area and each object's hitbox in `update()` |
| Scoring (increase and decrease) | `on_catch()`, `hit_hazard()` and `complete_order()` |
| Difficulty progression | Every bouquet raises the level: faster objects, quicker spawning, more weeds and bees, and bigger orders with more flower types |
| Game states | `MENU`, `PLAYING`, `PAUSED`, `GAME_OVER` (plus a short celebration pause after each bouquet) |
| Multimedia | Generated flower sprites and scenery (images), sound effects, looping background music, animations |
| Customization | Wind Gust event (see section 3) |
| Restart without relaunching | `start_game()` calls `reset()` |
| Bonus | High score saved to `highscore.txt` between sessions |

---

## 5. Project Structure

```
bloom_bouquet/
├── bloom_bouquet.py    # the entire game
├── README.md           # this file
├── requirements.txt    # pygame>=2.0
└── highscore.txt       # created automatically after your first game over
```

Main parts of the code:

- `CONFIG`: personalization settings
- `Audio`: generates and plays sound effects and music (works silently if no audio device exists)
- `draw_flower_head()`, `make_*_sprite()`, `draw_bouquet()`: draw every sprite and the finished bouquet with Pygame shapes
- `Faller`, `Particle`, `FloatText`, `WindPetal`: game object classes
- `Game`: state machine with `handle_event()`, `update()`, `draw()` and `run()`

---

## 6. Troubleshooting

- **No sound:** check your system volume and make sure `M` hasn't muted the game. If no audio device is found, the game runs without sound.
- **`ModuleNotFoundError: pygame`:** run `pip install pygame` (or `python -m pip install pygame`).
- **Game runs slowly:** close other heavy programs. The game targets 60 FPS.
