import pygame as pg

# Game settings
TITLE = "New Game"
SPRITESHEET = "char_anim.png"

# define colors
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
HEIGHT = 786    # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
FONT_NAME = 'arial'
# HS_FILE = "highscore.txt"

TILESIZE = 32   # Larger tilesize = closer camera
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'wall_rock_mid1.png'
GRASS_IMG = 'grass.png'

# Player settings
PLAYER_SPEED = 300
PLAYER_IMG = 'walk_fr0.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)