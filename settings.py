import pygame as pg

# Game settings
TITLE = "New Game"
SPRITESHEET = 'char_anim.png'
SPIDERSHEET = 'spidersheet.png'
WATERSHEET_B = 'falls_b64.png'
WATERSHEET_T = 'falls_t64.png'

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
DIFFBLUE = (51, 153, 255)
BROWN = (106, 55, 5)
BGCOLOR = BROWN

WIDTH = 1024    # 16 * 64 or 32 * 32 or 64 * 16
WD2 = WIDTH / 2
HEIGHT = 786    # 16 * 48 or 32 * 24 or 64 * 12
HD2 = HEIGHT / 2
FPS = 60

# FONT_NAME = 'arial'

TILESIZE = 64   # Larger tilesize = closer camera
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WATER_HIT_RECT = pg.Rect(0, 0, 28, 28)
COVER_HIT_RECT = pg.Rect(0, 0, 28, 28)
BLANK_IMG = 'blank_tile.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
COVER_LAYER = 2
MOB_LAYER = 2
EFFECTS_LAYER = 3
ITEMS_LAYER = 1

# Player settings
PLAYER_SPEED = 300
PLAYER_IMG = 'walk_fr0.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 28, 28)
PLAYER_ATK = ['swish-7.wav', 'swish-9.wav', 'swish-10.wav']

# Mob settings
MOB_HEALTH = 100
MOB_DMG = 10
MOB_IMG = 'spider_fr1.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400
SPLAT = 'splat6.png'

# Sound settings
BG_MUSIC = 'woods1.ogg'
