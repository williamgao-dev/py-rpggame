import pygame as pg
import random
import pytweening as tween
vec = pg.math.Vector2
DEBUG_MODE = "OFF"
DEBUG_DRAW_GRID = "OFF"
DEBUG_LIGHT = "OFF"

ALL_DEBUG = "OFF"
if ALL_DEBUG == "ON":
    DEBUG_MODE = "ON"
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
TILESIZE = 64
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_SPEED = 300
PLAYER_HEALTH = 150
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
# Offset of bullets coming out of the player so it looks like it comes out of the actual gun
BARREL_OFFSET = vec(30, 10)
# Player will be pushed back when shooting (KICKBACK)
KICKBACK = 200

# Mob settings`
MOB_IMG = 'zombie1_hold.png'
MOB_DEATH = 'splat green.png'
MOB_SPEED = random.choice([150, 100, 75, 125, 50])
MOB_HIT_RECT = pg.Rect(0,0,0,35)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 1000

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {
                    'bullet_speed': 500,
                    'bullet_lifetime': 1000,
                    'rate': 175,
                    'kickback': 200,
                    'spread': 5,
                    'damage': 13,
                    'bullet_size':'lg',
                    'bullet_count': 1
                    }
WEAPONS['shotgun'] = {
                    'bullet_speed': 400,
                    'bullet_lifetime': 500,
                    'rate': 900,
                    'kickback': 300,
                    'spread': 20,
                    'damage': 5,
                    'bullet_size': 'sm',
                    'bullet_count': 12
                    }

if DEBUG_MODE == "ON":
    BULLET_DAMAGE = MOB_HEALTH
else:
    BULLET_DAMAGE = 10

# VX
MUZZLE_FLASHES = ['puff1.png','puff2.png','puff3.png','puff4.png']
FLASH_DURATION = 40
DAMAGE_ALPHA = [i for i in range(0,255,25)]
NIGHT_COLOR = (15, 15, 15)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "lightsoft.png"

# Sprite layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
                'shotgun': 'obj_shotgun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
# The best looking bobbing style is the sine graph
BOB_STYLE = tween.easeInOutSine
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'], 'shotgun': ['shotgun.wav']}
WEAPON_SOUNDS_GUN = ['sfx_weapon_singleshot2.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}
