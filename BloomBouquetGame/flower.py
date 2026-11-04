import array
import math
import os
import random
import sys

import pygame

CONFIG = {
    "title": "BLOOM BOUQUET",
    "student_name": "Priyanka Dehariya",        
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

WIDTH, HEIGHT = 800, 600
FPS = 60
GROUND_Y = 535
HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")

MENU, PLAYING, PAUSED, GAME_OVER = "menu", "playing", "paused", "game_over"

WHITE = (255, 255, 255)
GOLD = (255, 215, 60)
RED = (230, 60, 60)
GREEN = (140, 255, 160)


FLOWERS = {
    "rose": ("Rose", (225, 40, 75)),
    "tulip": ("Tulip", (255, 130, 190)),
    "sunflower": ("Sunflower", (255, 200, 30)),
    "daisy": ("Daisy", (250, 250, 250)),
    "lavender": ("Lavender", (165, 115, 225)),
}


KIND_SPEED = {
    "rose": 1.0, "tulip": 1.0, "sunflower": 1.0, "daisy": 1.0, "lavender": 1.0,
    "weed": 1.0, "bee": 1.4, "wilted": 0.95, "dew": 0.9,
}


def I(v):
    return int(round(v))


RATE = 22050


def _tone(freq, dur, vol=0.4, slide=0.0):
    n = int(RATE * dur)
    buf = array.array("h")
    phase = 0.0
    for i in range(n):
        f = freq + slide * (i / RATE)
        phase += 2 * math.pi * f / RATE
        env = 1.0 - i / n
        buf.append(int(32767 * vol * env * math.sin(phase)))
    return buf


def make_sound(freq, dur, vol=0.4, slide=0.0):
    return pygame.mixer.Sound(buffer=_tone(freq, dur, vol, slide).tobytes())


def make_sequence(freqs, dur, vol=0.35):
    buf = array.array("h")
    for f in freqs:
        buf.extend(_tone(f, dur, vol))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_music():
    
    notes = [392, 440, 523, 587, 523, 440, 392, 330,
             392, 440, 523, 659, 587, 523, 440, 392]
    buf = array.array("h")
    for f in notes:
        buf.extend(_tone(f, 0.28, vol=0.10))
    return pygame.mixer.Sound(buffer=buf.tobytes())


class Audio:
   

    def __init__(self):
        self.enabled = True
        self.muted = False
        try:
            pygame.mixer.init(frequency=RATE, size=-16, channels=1, buffer=512)
            self.sfx = {
                "pick": make_sound(700, 0.14, 0.35, 700),
                "wrong": make_sound(240, 0.22, 0.4, -60),
                "hit": make_sound(170, 0.35, 0.6, -100),
                "dew": make_sound(900, 0.25, 0.35, -400),
                "wind": make_sound(260, 0.9, 0.2, 120),
                "done": make_sequence([523, 659, 784, 1047], 0.13),
                "start": make_sound(440, 0.3, 0.4, 500),
                "over": make_sound(420, 0.9, 0.5, -330),
            }
            self.music = make_music()
        except pygame.error:
            self.enabled = False

    def play(self, name):
        if self.enabled and not self.muted:
            self.sfx[name].play()

    def start_music(self):
        if self.enabled and not self.muted:
            self.music.play(loops=-1)

    def stop_music(self):
        if self.enabled:
            self.music.stop()

    def toggle_mute(self, music_should_play):
        if not self.enabled:
            return
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.stop()
        elif music_should_play:
            self.start_music()


def draw_flower_head(surf, kind, cx, cy, r):
   
    cx, cy = I(cx), I(cy)
    r = max(4, I(r))
    if kind == "daisy":
        for i in range(10):
            a = i * 2 * math.pi / 10
            p = (cx + I(math.cos(a) * r * 0.65), cy + I(math.sin(a) * r * 0.65))
            pygame.draw.circle(surf, (252, 252, 252), p, max(2, I(r * 0.38)))
            pygame.draw.circle(surf, (205, 205, 225), p, max(2, I(r * 0.38)), 1)
        pygame.draw.circle(surf, (255, 200, 40), (cx, cy), max(2, I(r * 0.42)))
    elif kind == "sunflower":
        for i in range(14):
            a = i * 2 * math.pi / 14
            p = (cx + I(math.cos(a) * r * 0.74), cy + I(math.sin(a) * r * 0.74))
            pygame.draw.circle(surf, (255, 200, 30), p, max(2, I(r * 0.30)))
            pygame.draw.circle(surf, (215, 150, 10), p, max(2, I(r * 0.30)), 1)
        pygame.draw.circle(surf, (120, 70, 25), (cx, cy), max(2, I(r * 0.52)))
        for i in range(6):
            a = i * 2 * math.pi / 6
            pygame.draw.circle(surf, (80, 45, 15),
                               (cx + I(math.cos(a) * r * 0.28), cy + I(math.sin(a) * r * 0.28)), 1)
    elif kind == "rose":
        pygame.draw.circle(surf, (165, 18, 48), (cx, cy), r)
        pygame.draw.circle(surf, (225, 40, 75), (cx, cy), max(2, I(r * 0.82)))
        pygame.draw.circle(surf, (190, 25, 55), (cx, cy), max(2, I(r * 0.60)))
        pygame.draw.circle(surf, (240, 75, 105), (cx, cy), max(2, I(r * 0.42)))
        pygame.draw.circle(surf, (165, 18, 48), (cx, cy), max(2, I(r * 0.20)))
        k = max(2, I(r * 0.5))
        pygame.draw.arc(surf, (140, 12, 40), pygame.Rect(cx - k, cy - k, 2 * k, 2 * k), 0.4, 4.2, 2)
    elif kind == "tulip":
        pts = [(cx - r * 0.9, cy - r * 0.2), (cx - r * 0.55, cy - r * 1.0), (cx, cy - r * 0.3),
               (cx + r * 0.55, cy - r * 1.0), (cx + r * 0.9, cy - r * 0.2),
               (cx + r * 0.6, cy + r * 0.85), (cx - r * 0.6, cy + r * 0.85)]
        pygame.draw.polygon(surf, (240, 100, 165), [(I(x), I(y)) for x, y in pts])
        pygame.draw.ellipse(surf, (255, 160, 205),
                            pygame.Rect(cx - I(r * 0.42), cy - I(r * 0.85), I(r * 0.84), I(r * 1.6)))
        pygame.draw.polygon(surf, (200, 70, 130), [(I(x), I(y)) for x, y in pts], 2)
    elif kind == "lavender":
        for j in range(7):
            y = cy - r + j * I(r * 0.34)
            off = -I(r * 0.22) if j % 2 == 0 else I(r * 0.22)
            col = (150, 100, 215) if j % 2 == 0 else (185, 140, 240)
            pygame.draw.circle(surf, col, (cx + off, y), max(2, I(r * 0.27)))
        pygame.draw.circle(surf, (185, 140, 240), (cx, cy - r), max(2, I(r * 0.22)))


def make_flower_sprite(kind):
    s = pygame.Surface((48, 72), pygame.SRCALPHA)
    pygame.draw.line(s, (50, 140, 60), (24, 40), (24, 70), 4)
    pygame.draw.ellipse(s, (70, 170, 75), pygame.Rect(26, 52, 16, 8))
    draw_flower_head(s, kind, 24, 23, 19 if kind != "lavender" else 17)
    return s


def make_wilted_sprite():
    s = pygame.Surface((48, 72), pygame.SRCALPHA)
    pygame.draw.lines(s, (110, 120, 60), False, [(24, 70), (25, 52), (34, 42)], 4)
    for i in range(8):
        a = i * 2 * math.pi / 8
        pygame.draw.circle(s, (120, 85, 55), (36 + I(math.cos(a) * 9), 44 + I(math.sin(a) * 9) + 3), 6)
    pygame.draw.circle(s, (75, 50, 30), (36, 47), 6)
    return s


def make_weed_sprite():
    s = pygame.Surface((50, 50), pygame.SRCALPHA)
    for i in range(12):
        a = i * 2 * math.pi / 12
        pygame.draw.line(s, (40, 110, 40), (25, 25),
                         (25 + I(math.cos(a) * 24), 25 + I(math.sin(a) * 24)), 4)
    pygame.draw.circle(s, (55, 140, 50), (25, 25), 15)
    pygame.draw.circle(s, (85, 175, 70), (21, 21), 6)
    pygame.draw.circle(s, (30, 80, 30), (25, 25), 15, 2)
    return s


def make_bee_sprites():
    frames = []
    for wing_up in (True, False):
        s = pygame.Surface((50, 42), pygame.SRCALPHA)
        wy = 4 if wing_up else 12
        pygame.draw.ellipse(s, (200, 230, 255, 190), pygame.Rect(10, wy, 14, 18))
        pygame.draw.ellipse(s, (200, 230, 255, 190), pygame.Rect(26, wy, 14, 18))
        pygame.draw.ellipse(s, (255, 205, 40), pygame.Rect(8, 18, 34, 20))
        for x in (18, 26, 34):
            pygame.draw.line(s, (30, 25, 20), (x, 19), (x, 36), 4)
        pygame.draw.ellipse(s, (30, 25, 20), pygame.Rect(8, 18, 34, 20), 2)
        pygame.draw.circle(s, (30, 25, 20), (41, 28), 3)
        pygame.draw.polygon(s, (30, 25, 20), [(8, 28), (1, 26), (1, 30)])
        frames.append(s)
    return frames


def make_dew_sprite():
    s = pygame.Surface((34, 44), pygame.SRCALPHA)
    pygame.draw.polygon(s, (90, 170, 250), [(17, 2), (30, 28), (4, 28)])
    pygame.draw.circle(s, (90, 170, 250), (17, 28), 13)
    pygame.draw.circle(s, (150, 210, 255), (17, 28), 13, 2)
    pygame.draw.circle(s, WHITE, (12, 25), 3)
    return s


def make_heart_sprite(size=26):
    s = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 70, 110), (11, 12), 9)
    pygame.draw.circle(s, (255, 70, 110), (25, 12), 9)
    pygame.draw.polygon(s, (255, 70, 110), [(3, 16), (33, 16), (18, 34)])
    pygame.draw.circle(s, (255, 170, 190), (9, 9), 3)
    return pygame.transform.smoothscale(s, (size, size))


def make_basket_sprite():
    s = pygame.Surface((100, 66), pygame.SRCALPHA)
    pygame.draw.arc(s, (130, 85, 40), pygame.Rect(22, 0, 56, 56), 0, math.pi, 5)
    pygame.draw.polygon(s, (170, 115, 60), [(6, 26), (94, 26), (82, 64), (18, 64)])
    for y in range(32, 64, 8):
        pygame.draw.line(s, (130, 85, 40), (8 + (y - 26) // 3, y), (92 - (y - 26) // 3, y), 2)
    for x in range(14, 90, 12):
        pygame.draw.line(s, (200, 150, 90), (x, 28), (x + (50 - x) // 6, 62), 2)
    pygame.draw.rect(s, (140, 92, 45), pygame.Rect(2, 22, 96, 9), border_radius=4)
    pygame.draw.rect(s, (95, 60, 28), pygame.Rect(2, 22, 96, 9), 2, border_radius=4)
    return s


def draw_bouquet(surf, kinds, cx, base_y, scale=1.0):
    """Draw a fan-shaped bouquet from a list of flower keys."""
    n = len(kinds)
    heads = []
    for i, k in enumerate(kinds):
        t = (i / (n - 1) - 0.5) * 2 if n > 1 else 0.0
        ang = math.radians(t * 55)
        length = (95 + (i % 2) * 22) * scale
        hx = cx + math.sin(ang) * length
        hy = base_y - math.cos(ang) * length
        pygame.draw.line(surf, (50, 140, 60), (I(cx), I(base_y)), (I(hx), I(hy)), max(2, I(4 * scale)))
        heads.append((hy, k, hx))
    # leaves
    for sign in (-1, 1):
        pygame.draw.ellipse(surf, (70, 170, 75),
                            pygame.Rect(I(cx + sign * 38 * scale - 18 * scale), I(base_y - 60 * scale),
                                        I(36 * scale), I(16 * scale)))
    for hy, k, hx in sorted(heads):
        draw_flower_head(surf, k, hx, hy, 21 * scale)
    paper = [(cx - 40 * scale, base_y - 28 * scale), (cx + 40 * scale, base_y - 28 * scale),
             (cx + 9 * scale, base_y + 72 * scale), (cx - 9 * scale, base_y + 72 * scale)]
    paper = [(I(x), I(y)) for x, y in paper]
    pygame.draw.polygon(surf, (250, 235, 215), paper)
    pygame.draw.polygon(surf, (215, 190, 165), paper, 2)
    rc = CONFIG["ribbon_color"]
    by = I(base_y - 6 * scale)
    pygame.draw.polygon(surf, rc, [(I(cx), by), (I(cx - 26 * scale), by - I(14 * scale)),
                                   (I(cx - 26 * scale), by + I(14 * scale))])
    pygame.draw.polygon(surf, rc, [(I(cx), by), (I(cx + 26 * scale), by - I(14 * scale)),
                                   (I(cx + 26 * scale), by + I(14 * scale))])
    pygame.draw.circle(surf, tuple(max(0, c - 40) for c in rc), (I(cx), by), max(3, I(6 * scale)))


class Faller:
    def __init__(self, kind, x, speed, sprites):
        self.kind = kind
        self.x = float(x)
        self.y = -40.0
        self.speed = speed
        self.phase = random.uniform(0, 6.28)
        self.angle = 0.0
        self.spin = random.uniform(-120, 120) if kind == "weed" else 0.0
        self.sprite = sprites[kind]
        self.image = self.sprite[0] if kind == "bee" else self.sprite
        self.rect = self.image.get_rect(center=(I(self.x), I(self.y)))
        self.hazard = kind in ("weed", "bee")

    def update(self, dt, mult, wind, t):
        self.y += self.speed * mult * dt
        self.x += wind * 0.9 * dt
        if self.kind == "bee":
            self.x += math.sin(t * 5 + self.phase) * 140 * dt
        self.x = max(26, min(WIDTH - 26, self.x))

        base = self.sprite
        if self.kind == "bee":
            base = self.sprite[int(t * 14) % 2]
        if self.kind == "weed":
            self.angle += self.spin * dt
        elif self.kind in FLOWERS or self.kind == "wilted":
            self.angle = math.sin(t * 3 + self.phase) * 18
        if self.kind == "weed" or self.kind in FLOWERS or self.kind == "wilted":
            self.image = pygame.transform.rotate(base, self.angle)
        else:
            self.image = base
        self.rect = self.image.get_rect(center=(I(self.x), I(self.y)))

    def hitbox(self):
        return self.rect.inflate(-self.rect.w * 0.35, -self.rect.h * 0.30)


class Particle:
    def __init__(self, x, y, color):
        a = random.uniform(0, 2 * math.pi)
        v = random.uniform(60, 240)
        self.x, self.y = x, y
        self.vx, self.vy = math.cos(a) * v, math.sin(a) * v - 60
        self.life = self.max_life = random.uniform(0.4, 0.9)
        self.color = color

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 220 * dt
        self.life -= dt

    def draw(self, surf):
        k = max(0.0, self.life / self.max_life)
        pygame.draw.circle(surf, self.color, (I(self.x), I(self.y)), max(1, I(5 * k)))


class FloatText:
    def __init__(self, text, x, y, color, font):
        self.img = font.render(text, True, color)
        self.x, self.y = x, y
        self.life = 1.0

    def update(self, dt):
        self.y -= 50 * dt
        self.life -= dt

    def draw(self, surf):
        self.img.set_alpha(I(255 * max(0.0, min(1.0, self.life))))
        surf.blit(self.img, self.img.get_rect(center=(I(self.x), I(self.y))))


class WindPetal:
    def __init__(self, direction):
        self.x = -20 if direction > 0 else WIDTH + 20
        self.y = random.randint(110, GROUND_Y - 20)
        self.vx = direction * random.uniform(320, 520)
        self.phase = random.uniform(0, 6.28)
        self.color = random.choice([(255, 170, 200), (255, 255, 255), (130, 200, 110), (255, 220, 120)])

    def update(self, dt, t):
        self.x += self.vx * dt
        self.y += math.sin(t * 6 + self.phase) * 60 * dt

    def alive(self):
        return -40 < self.x < WIDTH + 40

    def draw(self, surf):
        pygame.draw.ellipse(surf, self.color, pygame.Rect(I(self.x), I(self.y), 12, 7))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CONFIG["title"])
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.f_title = pygame.font.SysFont("arial", 62, bold=True)
        self.f_big = pygame.font.SysFont("arial", 38, bold=True)
        self.f_med = pygame.font.SysFont("arial", 26, bold=True)
        self.f_small = pygame.font.SysFont("arial", 19, bold=True)
        self.f_tiny = pygame.font.SysFont("arial", 16, bold=True)

        self.audio = Audio()
        self.build_assets()
        self.background = self.make_background()
        self.clouds = [[random.randint(0, WIDTH), random.randint(110, 300),
                        random.uniform(8, 22), random.uniform(0.7, 1.4)] for _ in range(5)]

        self.high_score = self.load_high_score()
        self.state = MENU
        self.menu_time = 0.0
        self.new_record = False
        self.reset()

    def build_assets(self):
        self.sprites = {k: make_flower_sprite(k) for k in FLOWERS}
        self.sprites["wilted"] = make_wilted_sprite()
        self.sprites["weed"] = make_weed_sprite()
        self.sprites["bee"] = make_bee_sprites()
        self.sprites["dew"] = make_dew_sprite()
        self.icons = {k: pygame.transform.smoothscale(self.sprites[k], (28, 42)) for k in FLOWERS}
        self.basket_img = make_basket_sprite()
        self.heart = make_heart_sprite(26)

    def make_background(self):
        bg = pygame.Surface((WIDTH, HEIGHT))
        top, bot = CONFIG["sky_top"], CONFIG["sky_bottom"]
        for y in range(GROUND_Y):
            t = y / GROUND_Y
            col = tuple(I(top[i] + (bot[i] - top[i]) * t) for i in range(3))
            pygame.draw.line(bg, col, (0, y), (WIDTH, y))
       
        pygame.draw.circle(bg, (255, 245, 190), (690, 150), 62)
        pygame.draw.circle(bg, (255, 232, 130), (690, 150), 42)
  
        g = CONFIG["grass_color"]
        far = tuple(min(255, c + 35) for c in g)
        pygame.draw.ellipse(bg, far, pygame.Rect(-120, 420, 560, 260))
        pygame.draw.ellipse(bg, tuple(min(255, c + 18) for c in g), pygame.Rect(300, 440, 640, 260))
     
        pygame.draw.rect(bg, g, pygame.Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        dark = tuple(max(0, c - 30) for c in g)
        rnd = random.Random(7)
        for _ in range(140):
            x = rnd.randint(0, WIDTH)
            y = rnd.randint(GROUND_Y + 4, HEIGHT - 4)
            pygame.draw.line(bg, dark, (x, y), (x + rnd.randint(-3, 3), y - rnd.randint(5, 11)), 2)
        for _ in range(26):
            x = rnd.randint(0, WIDTH)
            y = rnd.randint(GROUND_Y + 10, HEIGHT - 8)
            pygame.draw.circle(bg, rnd.choice([(255, 255, 255), (255, 190, 215), (255, 225, 110)]), (x, y), 3)
        # picket fence
        for x in range(0, WIDTH, 34):
            pygame.draw.rect(bg, (250, 245, 235), pygame.Rect(x + 4, GROUND_Y - 38, 20, 44))
            pygame.draw.polygon(bg, (250, 245, 235), [(x + 4, GROUND_Y - 38), (x + 14, GROUND_Y - 50), (x + 24, GROUND_Y - 38)])
            pygame.draw.rect(bg, (205, 195, 180), pygame.Rect(x + 4, GROUND_Y - 38, 20, 44), 1)
        pygame.draw.rect(bg, (235, 228, 215), pygame.Rect(0, GROUND_Y - 24, WIDTH, 7))
        return bg

    def reset(self):
        self.score = 0
        self.lives = CONFIG["start_lives"]
        self.elapsed = 0.0
        self.bouquets = 0
        self.level = 1
        self.spawn_timer = 0.5
        self.fallers = []
        self.particles = []
        self.floats = []
        self.petals = []
        self.invuln = 0.0
        self.shake = 0.0
        self.celebrate = 0.0
        self.last_bouquet = []
        self.last_bonus = 0
        self.wind_clock = 0.0
        self.wind_left = 0.0
        self.wind_dir = 1
        self.wind_force = 0.0
        self.player_x = WIDTH / 2
        self.use_mouse = False
        self.order = {}
        self.have = {}
        self.collected = []
        self.order_time = 0.0
        self.order_max = 1.0
        self.new_order()

    def new_order(self):
        n_types = min(5, 2 + self.bouquets // 2)
        max_count = 2 if self.bouquets < 3 else 3
        types = random.sample(list(FLOWERS), n_types)
        self.order = {k: random.randint(1, max_count) for k in types}
        self.have = {k: 0 for k in types}
        self.collected = []
        total = sum(self.order.values())
        self.order_max = min(75.0, CONFIG["order_time_base"] + total * CONFIG["order_time_per_flower"])
        self.order_time = self.order_max

    def load_high_score(self):
        try:
            with open(HIGHSCORE_FILE) as f:
                return int(f.read().strip())
        except (OSError, ValueError):
            return 0

    def save_high_score(self):
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(self.high_score))
        except OSError:
            pass

  
    def start_game(self):
        self.reset()
        self.state = PLAYING
        self.audio.play("start")
        self.audio.start_music()

    def end_game(self):
        self.state = GAME_OVER
        self.audio.stop_music()
        self.audio.play("over")
        self.new_record = self.score > self.high_score
        if self.new_record:
            self.high_score = self.score
            self.save_high_score()

   
    def handle_event(self, e):
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_m:
                self.audio.toggle_mute(self.state == PLAYING)
            if self.state == MENU:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif self.state == PLAYING:
                if e.key in (pygame.K_p, pygame.K_ESCAPE):
                    self.state = PAUSED
                    self.audio.stop_music()
                elif e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    self.use_mouse = False
            elif self.state == PAUSED:
                if e.key in (pygame.K_p, pygame.K_ESCAPE, pygame.K_RETURN):
                    self.state = PLAYING
                    self.audio.start_music()
            elif self.state == GAME_OVER:
                if e.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()
                elif e.key == pygame.K_ESCAPE:
                    self.state = MENU

        if e.type == pygame.MOUSEMOTION and self.state == PLAYING:
            self.use_mouse = True
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.state in (MENU, GAME_OVER):
                self.start_game()
            elif self.state == PAUSED:
                self.state = PLAYING
                self.audio.start_music()

    
    def basket_rect(self):
        return self.basket_img.get_rect(midbottom=(I(self.player_x), HEIGHT - 12))

    def catch_rect(self):
        r = self.basket_rect()
        return pygame.Rect(r.x + 12, r.y + 10, r.w - 24, 22)

    def spawn(self):
        lvl = self.level
        cats = ["flower", "weed", "bee", "wilted", "dew"]
        weights = [60, 10 + min(lvl * 2, 14), 4 + min(lvl * 2, 12), 9, 4]
        cat = random.choices(cats, weights)[0]
        if cat == "flower":
            needed = [k for k in self.order if self.have.get(k, 0) < self.order[k]]
            if needed and random.random() < 0.6:
                kind = random.choice(needed)
            else:
                kind = random.choice(list(FLOWERS))
        else:
            kind = cat
        speed = (135 + lvl * 14) * KIND_SPEED[kind] * random.uniform(0.85, 1.2)
        self.fallers.append(Faller(kind, random.randint(30, WIDTH - 30), speed, self.sprites))

    def update_clouds(self, dt):
        boost = 3.0 if self.wind_left > 0 else 1.0
        for c in self.clouds:
            c[0] += c[2] * dt * boost * self.wind_dir
            if c[0] > WIDTH + 100:
                c[0] = -100
            elif c[0] < -100:
                c[0] = WIDTH + 100

    def update_effects(self, dt):
        for p in self.particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.particles.remove(p)
        for ft in self.floats[:]:
            ft.update(dt)
            if ft.life <= 0:
                self.floats.remove(ft)
        t = pygame.time.get_ticks() / 1000.0
        for wp in self.petals[:]:
            wp.update(dt, t)
            if not wp.alive():
                self.petals.remove(wp)
        self.shake = max(0.0, self.shake - dt)
        self.invuln = max(0.0, self.invuln - dt)

    def update(self, dt):
        self.update_clouds(dt)
        if self.state == MENU:
            self.menu_time += dt
            return
        if self.state != PLAYING:
            return

        t = pygame.time.get_ticks() / 1000.0
        self.elapsed += dt
        self.level = 1 + self.bouquets

        keys = pygame.key.get_pressed()
        speed = 540
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += speed * dt
        if self.use_mouse:
            mx = pygame.mouse.get_pos()[0]
            self.player_x += (mx - self.player_x) * min(1.0, 14 * dt)
        self.player_x = max(52, min(WIDTH - 52, self.player_x))

        if self.celebrate > 0:
            self.celebrate -= dt
            if random.random() < 0.6:
                self.burst(random.randint(250, 550), random.randint(200, 420),
                           random.choice([(255, 215, 60), (255, 150, 200), (255, 255, 255)]), 2)
            self.update_effects(dt)
            if self.celebrate <= 0:
                self.new_order()
            return

        if self.wind_left > 0:
            self.wind_left -= dt
            progress = 1.0 - max(0.0, self.wind_left) / CONFIG["wind_duration"]
            self.wind_force = self.wind_dir * CONFIG["wind_strength"] * math.sin(math.pi * min(1.0, progress))
            if random.random() < 0.55:
                self.petals.append(WindPetal(self.wind_dir))
            if self.wind_left <= 0:
                self.wind_force = 0.0
        else:
            self.wind_clock += dt
            if self.wind_clock >= CONFIG["wind_every"]:
                self.wind_clock = 0.0
                self.wind_left = CONFIG["wind_duration"]
                self.wind_dir = random.choice([-1, 1])
                self.audio.play("wind")

       
        self.order_time -= dt
        if self.order_time <= 0:
            self.lives -= 1
            self.shake = 0.35
            self.popup("TIME'S UP!", WIDTH // 2, 190, RED)
            self.audio.play("hit")
            self.new_order()

       
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn()
            self.spawn_timer = max(0.28, 0.85 - (self.level - 1) * 0.05)

        
        mult = 1.0 + (self.level - 1) * 0.06
        catch = self.catch_rect()
        for f in self.fallers[:]:
            f.update(dt, mult, self.wind_force, t)
            if f.rect.top > HEIGHT:
                self.fallers.remove(f)
                continue
            if catch.colliderect(f.hitbox()):
                self.fallers.remove(f)
                self.on_catch(f)
                if self.celebrate > 0:
                    break

        self.update_effects(dt)
        if self.lives <= 0:
            self.end_game()

    def burst(self, x, y, color, n=14):
        for _ in range(n):
            self.particles.append(Particle(x, y, color))

    def popup(self, text, x, y, color):
        self.floats.append(FloatText(text, x, y, color, self.f_small))

    def on_catch(self, f):
        x, y = f.rect.center
        k = f.kind
        if k in FLOWERS:
            if self.have.get(k, 0) < self.order.get(k, 0):
                self.have[k] += 1
                self.collected.append(k)
                self.score += 10
                self.burst(x, y, FLOWERS[k][1])
                self.popup("+10", x, y, GOLD)
                self.audio.play("pick")
                if all(self.have[t] >= n for t, n in self.order.items()):
                    self.complete_order()
            else:
                self.score = max(0, self.score - 5)
                self.burst(x, y, (150, 150, 150), 8)
                self.popup("Not in order -5", x, y, (200, 90, 90))
                self.audio.play("wrong")
        elif k == "wilted":
            self.score = max(0, self.score - 10)
            self.burst(x, y, (120, 85, 55), 12)
            if self.collected:
                lost = self.collected.pop()
                self.have[lost] -= 1
                self.popup("Wilted! -1 flower", x, y, (190, 120, 70))
            else:
                self.popup("Wilted -10", x, y, (190, 120, 70))
            self.audio.play("wrong")
        elif k == "dew":
            self.order_time = min(self.order_max, self.order_time + 8)
            self.burst(x, y, (120, 190, 255))
            self.popup("+8 sec", x, y, (130, 200, 255))
            self.audio.play("dew")
        elif f.hazard:
            self.hit_hazard(x, y, k)

    def hit_hazard(self, x, y, kind):
        if self.invuln > 0:
            return
        self.lives -= 1
        self.score = max(0, self.score - 10)
        self.invuln = 1.2
        self.shake = 0.35
        self.burst(x, y, (255, 200, 60) if kind == "bee" else (70, 150, 60), 22)
        self.popup("OUCH! -10", x, y, RED)
        self.audio.play("hit")

    def complete_order(self):
        bonus = 50 + I(self.order_time) * 2
        self.score += bonus
        self.bouquets += 1
        self.last_bouquet = list(self.collected)
        self.last_bonus = bonus
        self.celebrate = 2.8
        self.fallers.clear()
        self.audio.play("done")

    
    def draw_text(self, text, font, color, center=None, topleft=None, topright=None, shadow=True):
        img = font.render(text, True, color)
        r = img.get_rect()
        if center:
            r.center = center
        if topleft:
            r.topleft = topleft
        if topright:
            r.topright = topright
        if shadow:
            sh = font.render(text, True, (0, 0, 0))
            sh.set_alpha(110)
            self.screen.blit(sh, (r.x + 2, r.y + 2))
        self.screen.blit(img, r)
        return r

    def draw_cloud(self, c):
        x, y, _, s = c
        for dx, dy, rr in ((0, 0, 26), (26, -8, 32), (58, 0, 26), (28, 8, 24)):
            pygame.draw.circle(self.screen, (255, 255, 255), (I(x + dx * s), I(y + dy * s)), I(rr * s))

    def draw_basket(self, t):
        r = self.basket_rect()
        if self.invuln > 0 and int(t * 14) % 2 == 0:
            return
      
        shown = self.collected[-6:]
        for i, k in enumerate(shown):
            fx = r.x + 22 + i * 11 + (i % 2) * 3
            fy = r.y + 8 - (i % 3) * 7
            pygame.draw.line(self.screen, (50, 140, 60), (fx, fy + 4), (fx, r.y + 24), 3)
            draw_flower_head(self.screen, k, fx, fy, 11)
        self.screen.blit(self.basket_img, r)

    def draw_order_card(self):
        card = pygame.Rect(205, 4, 390, 98)
        panel = pygame.Surface(card.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (35, 55, 40, 190), panel.get_rect(), border_radius=12)
        pygame.draw.rect(panel, (255, 240, 200, 230), panel.get_rect(), 2, border_radius=12)
        self.screen.blit(panel, card.topleft)
        self.draw_text(f"BOUQUET ORDER #{self.bouquets + 1}", self.f_tiny, GOLD, center=(card.centerx, 17))

        n = len(self.order)
        slot_w = 76
        x0 = card.centerx - (n * slot_w) // 2
        for i, (k, need) in enumerate(self.order.items()):
            sx = x0 + i * slot_w
            have = self.have.get(k, 0)
            self.screen.blit(self.icons[k], (sx + 4, 28))
            done = have >= need
            self.draw_text(f"{have}/{need}", self.f_small, GREEN if done else WHITE,
                           center=(sx + 52, 50))
            if done:
                self.draw_text("OK", self.f_tiny, GREEN, center=(sx + 52, 68))

        frac = max(0.0, self.order_time / self.order_max)
        bar = pygame.Rect(card.x + 12, card.bottom - 14, card.w - 24, 8)
        pygame.draw.rect(self.screen, (30, 40, 30), bar, border_radius=4)
        col = (90, 210, 100) if frac > 0.5 else ((240, 200, 60) if frac > 0.25 else (235, 80, 70))
        fill = bar.copy()
        fill.w = max(0, I(bar.w * frac))
        pygame.draw.rect(self.screen, col, fill, border_radius=4)

    def draw_hud(self):
        self.draw_text(f"SCORE {self.score}", self.f_med, WHITE, topleft=(14, 8))
        self.draw_text(f"BEST {self.high_score}", self.f_tiny, (250, 250, 250), topleft=(16, 40))
        self.draw_text(f"Bouquets: {self.bouquets}", self.f_small, (255, 235, 245), topleft=(16, 62))
        for i in range(self.lives):
            self.screen.blit(self.heart, (WIDTH - 38 - i * 30, 10))
        self.draw_text(f"LEVEL {self.level}", self.f_small, GOLD, topright=(WIDTH - 14, 42))
        mm, ss = divmod(I(self.elapsed), 60)
        self.draw_text(f"TIME {mm:02d}:{ss:02d}", self.f_tiny, WHITE, topright=(WIDTH - 14, 68))
        self.draw_order_card()
        if self.wind_left > 0:
            arrows = ">>>" if self.wind_dir > 0 else "<<<"
            self.draw_text(f"{arrows} WIND GUST {arrows}", self.f_small, (255, 255, 255),
                           center=(WIDTH // 2, 124))

    def draw_celebration(self, t):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((20, 30, 20, 120))
        self.screen.blit(ov, (0, 0))
        pulse = 1.0 + 0.04 * math.sin(t * 8)
        draw_bouquet(self.screen, self.last_bouquet, WIDTH // 2, 400, 1.5 * pulse)
        self.draw_text(f"BOUQUET #{self.bouquets} READY!", self.f_big, GOLD, center=(WIDTH // 2, 170))
        self.draw_text(f"Bonus +{self.last_bonus}", self.f_med, WHITE, center=(WIDTH // 2, 214))

    def draw_menu(self):
        t = self.menu_time
        bob = math.sin(t * 2) * 7
        self.draw_text(CONFIG["title"], self.f_title, (255, 250, 245), center=(WIDTH // 2, 70 + bob))
        self.draw_text("Catch flowers. Fill the order. Make the bouquet!", self.f_med, (255, 245, 250),
                       center=(WIDTH // 2, 125))

       
        panel = pygame.Surface((WIDTH - 60, 250), pygame.SRCALPHA)
        pygame.draw.rect(panel, (30, 55, 40, 150), panel.get_rect(), border_radius=14)
        self.screen.blit(panel, (30, 150))
        for i, k in enumerate(FLOWERS):
            x = 100 + i * 150
            self.screen.blit(self.sprites[k], self.sprites[k].get_rect(center=(x, 205)))
            self.draw_text(FLOWERS[k][0], self.f_tiny, WHITE, center=(x, 252))
        self.draw_text("Collect the flowers on the ORDER card:  +10 each", self.f_small, GOLD,
                       center=(WIDTH // 2, 278))

        hazards = [
            ("weed", "Weed  -1 life"),
            ("bee", "Bee  -1 life"),
            ("wilted", "Wilted  -1 flower"),
            ("dew", "Dew drop  +8 sec"),
        ]
        for i, (k, label) in enumerate(hazards):
            x = 110 + i * 190
            spr = self.sprites[k][0] if k == "bee" else self.sprites[k]
            spr = pygame.transform.smoothscale(spr, (I(spr.get_width() * 0.75), I(spr.get_height() * 0.75)))
            self.screen.blit(spr, spr.get_rect(center=(x - 30, 345)))
            self.draw_text(label, self.f_tiny, WHITE, topleft=(x + 2, 336))

        lines = [
            ("Move: LEFT / RIGHT or A / D or the MOUSE / touch", WHITE),
            ("Pause: P     Mute: M     Quit: ESC", WHITE),
            ("WIND GUSTS blow everything sideways - plan ahead!", (255, 250, 190)),
        ]
        for i, (ln, col) in enumerate(lines):
            self.draw_text(ln, self.f_small, col, center=(WIDTH // 2, 428 + i * 28))

        if int(t * 2) % 2 == 0:
            self.draw_text("Press ENTER or click to START", self.f_big, WHITE, center=(WIDTH // 2, 520))
        self.draw_text(f"Best: {self.high_score}", self.f_tiny, WHITE, topleft=(14, HEIGHT - 26))
        self.draw_text(f"By {CONFIG['student_name']}", self.f_tiny, WHITE, topright=(WIDTH - 14, HEIGHT - 26))

    def draw_pause(self):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((10, 25, 15, 170))
        self.screen.blit(ov, (0, 0))
        self.draw_text("PAUSED", self.f_title, WHITE, center=(WIDTH // 2, HEIGHT // 2 - 20))
        self.draw_text("Press P / ESC / ENTER to resume", self.f_med, (220, 240, 220),
                       center=(WIDTH // 2, HEIGHT // 2 + 40))

    def draw_game_over(self):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((25, 10, 20, 195))
        self.screen.blit(ov, (0, 0))
        self.draw_text("SHOP CLOSED", self.f_title, (255, 130, 150), center=(WIDTH // 2, 130))
        self.draw_text(f"Score: {self.score}", self.f_big, WHITE, center=(WIDTH // 2, 215))
        if self.new_record:
            self.draw_text("NEW HIGH SCORE!", self.f_med, GOLD, center=(WIDTH // 2, 262))
        else:
            self.draw_text(f"Best: {self.high_score}", self.f_med, (230, 230, 245), center=(WIDTH // 2, 262))
        self.draw_text(f"Bouquets made: {self.bouquets}   |   Time played: {I(self.elapsed)}s",
                       self.f_small, (230, 230, 245), center=(WIDTH // 2, 310))
        if self.last_bouquet:
            draw_bouquet(self.screen, self.last_bouquet, WIDTH // 2, 395, 0.8)
        self.draw_text("Press R / ENTER / click to PLAY AGAIN", self.f_med, WHITE, center=(WIDTH // 2, 520))
        self.draw_text("ESC - main menu", self.f_small, (200, 200, 225), center=(WIDTH // 2, 556))

    def draw(self):
        t = pygame.time.get_ticks() / 1000.0
        self.screen.blit(self.background, (0, 0))
        for c in self.clouds:
            self.draw_cloud(c)

        if self.state == MENU:
            self.draw_menu()
        else:
            for f in self.fallers:
                self.screen.blit(f.image, f.rect)
            self.draw_basket(t)
            for wp in self.petals:
                wp.draw(self.screen)
            for p in self.particles:
                p.draw(self.screen)
            for ft in self.floats:
                ft.draw(self.screen)
            self.draw_hud()
            if self.celebrate > 0:
                self.draw_celebration(t)
            if self.state == PAUSED:
                self.draw_pause()
            elif self.state == GAME_OVER:
                self.draw_game_over()

            if self.shake > 0:  # screen shake
                frame = self.screen.copy()
                self.screen.fill((0, 0, 0))
                self.screen.blit(frame, (random.randint(-6, 6), random.randint(-6, 6)))
        pygame.display.flip()

  
    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            for e in pygame.event.get():
                self.handle_event(e)
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    Game().run()