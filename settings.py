import pygame as pg

# Game settings
TITLE = "New Game"
START_TXT = "Press a key to start"
GO_TXT = "GAME OVER"

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
HT34 = HEIGHT * 3 / 4
FPS = 60

# FONT_NAME = 'arial'

TILESIZE = 64   # Larger tilesize = closer camera
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WATER_HIT_RECT = pg.Rect(0, 0, 28, 28)
COVER_HIT_RECT = pg.Rect(0, 0, 28, 28)
# BLANK_IMG = 'test.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
COVER_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 3
ITEMS_LAYER = 1

# Player settings
SPRITESHEET = 'char_anim.png'
P_ATK_SHEET = 'player_atk.png'
PLAYER_SPEED = 300
PLAYER_IMG = 'walk_fr0.png'
TEST_IMG = 'stand_fr_test.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 20, 25)
PLAYER_ATK = ['swish-7.wav', 'swish-9.wav', 'swish-10.wav']

PLAYER_HEALTH = 100
BAR_LENGTH = 100        # Health bar
BAR_HEIGHT = 20         # Health bar

# Mob settings
MOB_HEALTH = 100
MOB_DMG = 10
MOB_IMG = 'spider_fr1.png'
MOB_SPEEDS = [250, 200, 175, 225]
MOB_HIT_RECT = pg.Rect(0, 0, 60, 40)
MOB_KNOCKBACK = 30
AVOID_RADIUS = 50
DETECT_RADIUS = 400
SPLAT = 'splat6.png'

# Effects
DMG_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = 'gradient_mask2.png'


# Sound settings
BG_MUSIC = 'woods1.ogg'

# Foreground images
COVER_IMGS = {
    'grass_L': 'grass_L.png', 'grass_LU': 'grass_LU.png',
    'grass_LUR': 'grass_LUR.png', 'grass_R': 'grass_R.png',
    'grass_RD': 'grass_RD.png', 'grass_U': 'grass_U.png',
    'grass_UR': 'grass_UR.png', 'pineB-0': 'pineB-0.png',
    'pineB-1': 'pineB-1.png', 'pineB-2': 'pineB-2.png',
    'pineB-3': 'pineB-3.png', 'pineM-0': 'pineM-0.png',
    'pineM-1': 'pineM-1.png', 'pineM-2': 'pineM-2.png',
    'pineM-3': 'pineM-3.png', 'pineT-0': 'pineT-0.png',
    'pineT-1': 'pineT-1.png', 'pineT-2': 'pineT-2.png',
    'pineT-3': 'pineT-3.png', 'treeB-0': 'treeB-0.png',
    'treeB-1': 'treeB-1.png', 'treeB-2': 'treeB-2.png',
    'treeB-3': 'treeB-3.png', 'treeM-0': 'treeM-0.png',
    'treeM-1': 'treeM-1.png', 'treeM-2': 'treeM-2.png',
    'treeM-3': 'treeM-3.png', 'treeT-0': 'treeT-0.png',
    'treeT-1': 'treeT-1.png', 'treeT-2': 'treeT-2.png',
    'treeT-3': 'treeT-3.png', 'lone_pineT-0': 'lone_pineT-0.png',
    'lone_pineT-1': 'lone_pineT-1.png', 'lone_pineM-0': 'lone_pineM-0.png',
    'lone_pineM-1': 'lone_pineM-1.png', 'lone_pineB-0': 'lone_pineB-0.png',
    'lone_pineB-1': 'lone_pineB-1.png', 'lone_treeT-0': 'lone_treeT-0.png',
    'lone_treeT-1': 'lone_treeT-1.png', 'lone_treeM-0': 'lone_treeM-0.png',
    'lone_treeM-1': 'lone_treeM-1.png', 'lone_treeB-0': 'lone_treeB-0.png',
    'lone_treeB-1': 'lone_treeB-1.png', 'shrub_lg': 'shrub_lg.png',
    'shrub_sm': 'shrub_sm.png', 'sm_pine': 'sm_pine.png',
    'sm_tree': 'sm_tree.png'
}
