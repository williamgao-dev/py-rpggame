import pygame as pg

DEBUG_MODE = "OFF"
DRAW_GRID = "OFF"


# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (0,155,155)
DARKGREY = (40,40,40)
LIGHTGREY = (100,100,100)
BROWN = (106,55,5)

# Global variables
WIDTH = 1024 # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap"
BGCOLOR = BROWN

# Tilesize can be modified, however it needs to be a multiple of 32.
TILESIZE = 50
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_SPEED = 200
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)

# Mob settings
MOB_IMG = 'zombie1_hold.png'
