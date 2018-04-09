'''
    William Gao
    Project for Software Development and Design (2018, YR11)
    Top-down shooter
    Written in python, primarily using the pygame module

    Documentation throughout the entire project and its associated
    files in order to demonstrate my depth and understanding of the
    code being written. Explains what small parts of code does and
    its role in creating the game.

    The GitHub repo associated with this project, with
    commits to show my development throughout

    https://github.com/williamgao-dev/rpggame

    Credits:
    Game art / sprite art: http://kenney.nl/assets/topdown-shooter
'''


import pygame as pg
import random
from os import path
import pytweening as tween
import itertools
import pytmx

# Loading pygame vector class
vec = pg.math.Vector2

'''

    DEV SETTINGS (DEBUG)

'''

DEBUG_MODE = "OFF"
DEBUG_DRAW_GRID = "OFF"
DEBUG_LIGHT = "OFF"
ALL_DEBUG = "OFF"
if ALL_DEBUG == "ON":
    DEBUG_MODE = "ON"
    DRAW_GRID = "OFF"


'''

    SETTINGS


'''


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
# Radius in pixels in which zombies will be able to "see" players
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
                    'spread': 15,
                    'damage': 10,
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
NIGHT_COLOR = (50, 50, 50)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "lightsoft.png"

# Sprite layers (important)
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
# The best looking bobbing style is the sine graph :) (tweening & easing)
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

'''

    Game Class

'''

class Game:
    def __init__(self):
        # Initialize pygame, pg sounds & game window, etc
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Starts a timer - used to record events
        self.clock = pg.time.Clock()
        # pg.key.set_repeat(500,100) # Keyboard repeating function, (time key is held, time between repeats)
        # Ensures game remains running until set otherwise
        self.load_data()
        self.running = True

    def load_data(self):
        game_folder = path.dirname(__file__)

        # Assets folder initalization
        img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, 'maps')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')

        # Fonts
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')

        # Image to dim the screen
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        # Black, with alpha channel of 180
        self.dim_screen.fill((0,0,0,180))

        # Player image variable initalization
        # PLAYER_IMG is specified in the constants in settings.py
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()

        # Take the normal bullet image and scale it down to get smaller bullet images
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10,10))
        self.splat = pg.image.load(path.join(img_folder, MOB_DEATH)).convert_alpha()
        self.splat = pg.transform.scale(self.splat,(64,64))

        # List to store the animation pictures for gun muzzle
        self.gun_flashes = []
        # List to store the images for the items (e.g health_pack)
        self.item_images = {}
        # For each image in the list, append them to self.gun_flashes
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

        # Lighting effects (fog of war)
        self.fog = pg.Surface((WIDTH,HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        # Resize wall_img to match the wall size (tilesize)
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

        # All sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for sound in EFFECTS_SOUNDS:
            self.effects_sounds[sound] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[sound]))
        self.weapon_sounds = {}
        self.weapon_sounds['gun'] = []
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder,snd))
                s.set_volume(.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.15)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    # Quit function
    def quit(self):
        pg.quit()
        quit()

    # Called to initalize the game
    def new(self):
        self.paused = False

        # Initalizes the all_sprites and walls group
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()

        # Initalizing the TiledMap
        self.map = TiledMap(path.join(self.map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        '''

            Obselete code, unless the text based map generator is in use.

        '''
        # # Enumerate takes item AND index number <=== IMPORTANT!
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #
        #         # If tile is 1, spawn a Wall sprite at the x and y coordinates
        #         if tile == '1':
        #             Wall(self,col,row)
        #
        #         # If tile is P, spawn a Player sprite at the x and y coordinates
        #         if tile == 'P':
        #             self.player = Player(self,col,row)
        #
        #         # If tile is M, spawn a Player sprite at the x and y coordinates
        #         if tile == 'M':
        #             Mob(self,col,row)

        # Generation of the map through tilemap
        for object in self.map.tmxdata.objects:
            obj_center = vec(object.x + object.width/2,
                            object.y + object.height/2)
            if object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if object.name == 'wall':
                Obstacle(self,object.x,object.y,object.width,object.height)
            if object.name == 'zombie':
                Mob(self, obj_center, obj_center)
            if object.name in ['health','shotgun']:
                Item(self,obj_center, object.name)

        # For debugging purposes: ensures that the player spawns at 5,5 instead of relying on
        # tile management
        # self.player = Player(self,5,5)

        # Initalize the camera
        self.camera = Camera(self.map.width,self.map.height)
        self.effects_sounds['level_start'].play()
        if DEBUG_LIGHT == "ON":
            self.night = False
        else:
            self.night = True

    def run(self):
        # Game Loop, runs while self.playing = True
        self.playing = True

        # Infinitely looping BG music
        pg.mixer.music.play(loops=-1)
        while self.playing:

            # Delta time, difference in time, in seconds.
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    # Updates all groups every frame per second
    def update(self):

        # Check if the game is over. The condition for game over is when there
        # are no mobs left.
        if len(self.mobs) == 0:
            self.playing = False

        # Game Loop - Update
        self.all_sprites.update()

        # In every frame, update the camera to match the players offset.
        # THIS IS AMAZING! The camera sprite will follow whatever sprite you command
        # it to follow! In this case, we require the map to move with the camera.
        self.camera.update(self.player)

        # Player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            # If item is a health pack, AND the player is NOT on full health,
            # kill the sprite, and add (HEALTH_PACK_AMOUNT) to the players health (this is a function)
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'

        # If mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if DEBUG_MODE == "ON":
                if self.player.health <= 0:
                    self.player.health = 100
            else:
                if self.player.health <= 0:
                    self.playing = False

        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK,0).rotate(-hits[0].rot)

        # If bullets hit a mob
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)

        # 50% chance of a sound occuring in the event of the mob hitting a player
        for mob in hits:
            if random.random() < 0.5:
                random.choice(self.player_hit_sounds).play()

            # Remove BULLET_DAMAGE health from the mobs health
            #hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage

            # THIS IS AWESOME! Now the bullets have stopping power.
            mob.vel = vec(0,0)



    # Event handling
    def events(self):
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                self.quit()
            # Check for ESC key
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused

    # Function to draw gridmap for game window
    def draw_grid(self):
        # Draws vertical lines
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0),(x,HEIGHT))
        # Draws horizontal lines
        for y in range(0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY,(0,y),(WIDTH,y))

    # Rendering of the fog layer to make it look like night
    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        # Fog colour
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        # Apply light gradient
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog,(0,0),special_flags = pg.BLEND_MULT)

    # Blits and draws all stuff to screen
    def draw(self):
        # Makes the program title an fps counter if debugmode is on
        if DEBUG_MODE == "ON":
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            # Draws an outline on the hitbox of all sprite rectangles if debugmode is on
            if DEBUG_MODE == "ON":
                pg.draw.rect(self.screen, BLACK, self.camera.apply_rect(sprite.hit_rect), 1)
        # Draws an outline on the hitbox of all wall rectangles if debugmode is on
        if DEBUG_MODE == "ON":
            for wall in self.walls:
                pg.draw.rect(self.screen, BLACK, self.camera.apply_rect(wall.rect), 1)
        if DEBUG_DRAW_GRID == "ON":
            self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image,self.camera.apply(sprite))

        if self.night:
            self.render_fog()

        # This will draw a rect around the player hitbox (DEBUG_MODE)
        if DEBUG_MODE == "ON":
            pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        draw_player_health(self.screen, 10,10, self.player.health/PLAYER_HEALTH)
        self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE,
                       WIDTH - 10, 10, align="ne")

        # If game is paused, draw some text onto the screen
        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH/2, HEIGHT/2, align = "center")

        pg.display.flip()

    def show_start_screen(self):
        # Game splash/start screen
        pass

    def show_go_screen(self):
        # Gameover / continue dim_screen
        # Shows information, waits for player input
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH/2,
                        HEIGHT/2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH/2,
                        HEIGHT*3/4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        # Clears the queue of events
        pg.event.wait()
        waiting = True
        # If keyup, the game restarts
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    # Function to draw text onto the screen. (pretty useful)
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

# HUD Function
# Function to draw player health onto screen.
def draw_player_health(surf, x,y, percent):
    # Cannot have negative health
    if percent < 0:
        percent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = percent * BAR_LENGTH
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
    if percent > 0.6:
        col = GREEN
    elif percent > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf,WHITE,outline_rect,2)

def collide_with_walls(sprite, group, dir):

    '''
        My nifty little collision checker.
        Having TWO checks ensures that in event of one x or y value collision,
        Movement the other way still works, thus we can slide down walls.
        If direction is x, detect collisions.

        rect HIT_RECT is used for collisions instead of the normal rectangle
        as it provides more consistent collisions as it is a static rectangle
        unlike the rectangle surrounding the player sprite that's used to track
        movement

        This function is not a method of any class, which means that this function
        will work with any sprite, give the sprite, the group the collision checker
        must check with, and the direction.

    '''

    # If direction is x, perform collision checking for x axis
    if dir == 'x':
        # Detects collision between player and walls.
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # If hits == True.
        if hits:
            # If velocity is right,
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            # If velocity is left
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    # If direction is y, perform collision checking for y axis
    if dir == 'y':
        # Detects collision between player and walls.
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # If hits == True
        if hits:
            # If velocity is down
            if hits[0].rect.centery > sprite.hit_rect.centery > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            # If velocity is up
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

# Player sprite class
class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        # Setting layer
        self._layer = PLAYER_LAYER
        # Initalize an instance of Player in group all_sprites
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        # Sets attributes of class Player, sets a reference to the game class
        self.game = game
        # Sets the image that will be used for the player sprite to
        # the player image loaded in game.load_data
        self.image = game.player_img
        self.rect = self.image.get_rect()

        # This is actually a really important piece of code.
        # Without it, a bug will occur and prevent the player from spawning
        # where it is meant to be.
        #
        # This is because when we first init the class, if we do not define its
        # center, it will default to 0,0 then update. When we update, we check for
        # wall collisions, and there is a wall at 0,0 thus we will be pushed to the other
        # side of the wall, causing the player to not even be able to enter the map
        # and effectively stopping it from spawning where we actually intended it to
        # spawn.
        self.rect.center = (x,y)
        # <><><><><><><><><><><> #

        # Different rectangle for collision detection
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        # VECTORS
        # Velocity vector
        self.vel = vec(0,0)
        # Position vector
        self.pos = vec(x,y)
        self.rot = 0
        self.last_shot = 0
        # Set health
        self.health = PLAYER_HEALTH
        # Default weapon will be a pistol
        self.weapon = 'pistol'
        self.damaged = False

    # Function to get key presses, and move character in direction in event of keypress
    def get_keys(self):

        self.rot_speed = 0

        # Set vx and vy to 0 unless a key is pressed.

        self.vel = vec(0,0)

        # Event handling of keyboard input

        keys = pg.key.get_pressed()
        click = pg.mouse.get_pressed()

        # If left or right, make the character rotate at player_rot_speed
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED

        # If up or down, move up or down
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED,0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2,0).rotate(-self.rot)

        # Shoot when space is pressed
        if keys[pg.K_SPACE] or click[0] == 1:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()

        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)

            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spr = random.uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spr),WEAPONS[self.weapon]['damage'])
                snd = random.choice(self.game.weapon_sounds[self.weapon])

                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game,pos)

    def hit(self):
        self.damaged = True
        self.damage_alpha = itertools.chain(DAMAGE_ALPHA * 3)

    # Function that WILL executes at every frame of the game.
    def update(self):
        self.get_keys()

        # Transform the image of the player so it rotates
        # Rotates image around the centre to ensure consistent movement
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255,0,0, next(self.damage_alpha)), special_flags = pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()

        # Updating rotation (mod 360 means that we will always go back to 0 at 360 degrees)
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360

        # Note that I use hit_rect instead of the normal rectangle to ensure consistent collision
        # as the normal rect changes in proportion of the image in the middle, but this new one
        # is a constant rectangle thus the hitbox of the rectangle remains constant as well.

        # Updates x value
        self.hit_rect.centerx = self.pos.x

        # Calls collide_with_walls('x') every frame, checking if theres a collision
        collide_with_walls(self,self.game.walls,'x')

        # Update y value
        self.hit_rect.centery = self.pos.y

        # Calls collide_with_walls('y') every frame
        collide_with_walls(self,self.game.walls,'y')

        self.rect.center = self.hit_rect.center

    def add_health (self,amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

# Mob sprite class
class Mob(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        # Setting layer
        self._layer = MOB_LAYER
        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.mobs
        self.game = game

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.rot = 0
        self.health = 100
        self.speed = MOB_SPEED
        self.target = game.player

        # Vectors
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def avoid_mobs(self):
        # For each mob in mobs
        for mob in self.game.mobs:
            # Ignore current mob
            if mob != self:
                # Get the distance between current mob and mob in group
                dist = self.pos - mob.pos
                # If the distance between them is less than 50
                if 0 < dist.length() < AVOID_RADIUS:
                    # Spread them throughout a radius to avoid them clumping up
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        # The distance is calculated via pythag theorem
        # Getting the squared because calculations of square roots through
        # computers is extremely slow.
        # If the distance between the mob and the player is smaller than the
        # detection radius, make the mob move and do its usual stuff
        if target_dist.length_squared() < DETECT_RADIUS**2:
            if random.random() < 0.002:
                random.choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1,0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

            # Unit vector
            self.acc = vec(1,0).rotate(-self.rot)

            # Mechanism to prevent mobs from clumping. Refer to avoid_mobs for documentation
            self.avoid_mobs()

            # Use self.speed as MOB_SPEEDS has a bunch of varying speeds, meaning
            # zombies will have different speeds, instead of all them being statically
            # moving together
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self,self.game.walls,'y')

        if self.health <= 0:
            random.choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32,32))

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

# Bullet sprite class
class Bullet(pg.sprite.Sprite):
    def __init__(self,game,pos,dir,damage):
        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.bullets

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        # Setting layers
        self._layer = BULLET_LAYER

        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos

        # Add some randomness to the bullets being shot
        # This will make the bullets shoot on a slightly different offset every Bullet
        # spread =  random.uniform(-GUN_SPREAD, GUN_SPREAD)

        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * random.uniform(0.9,1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        # If the bullets lifetime exceeds its limit, it stops
        # This is to ensure that bullets don't fly forever.
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()
        # If bullet hits any wall, it stops.
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()

'''

    Obselete class. Only to be used when a text based map is being used as an alternative to a
    tilemap. Might be useful for debugging purposes.

'''
class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):

        # Setting layers
        self._layer = WALL_LAYER

        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.walls

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        # Attributes of the wall
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # Makes the wall the size of a tile
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Obstacle class
class Obstacle(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h):

        # Defines which groups the sprite should be in
        self.groups = game.walls

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        # Attributes of the Obstacle
        self.game = game
        self.rect = pg.Rect (x,y,w,h)

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y

# MuzzleFlass class to manage muzzle flashes (utility)
class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self,game,pos):
        # Setting layers
        self._layer = EFFECTS_LAYER

        # Defines which groups the sprite should be in
        self.groups = game.all_sprites

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        # Pass a copy of the game
        self.game = game

        # Attributes
        size = random.randint(20,50)
        self.image = pg.transform.scale(random.choice(game.gun_flashes),(size,size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
        self.hit_rect = self.rect

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self,game,pos,type):
        self._layer = ITEMS_LAYER

        # Defines which groups the sprite should be in
        self.groups = game.all_sprites,game.items

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        # Pass a copy of the game
        self.game = game

        # Attributes
        self.pos = pos
        self.type = type
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # Easing and tweening
        self.tween = BOB_STYLE
        self.step = 0
        self.dir = 1

    def update(self):
        # Bobbing motion using tweening and easing by BOB_STYLE
        # Every frame we calc how far along we are on the tween, as a percentage
        # of the total range, shifted by half the value, so we start in the middle
        # Then we add the offset to the rectangles position.
        # As we increment the step we get the maximum, we get to and then negative numbers
        # then the direction will change.
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)

"""

    Obselete function, use TiledMap instead unless debugging

"""
class Map:
    def __init__(self,filename):

        # Creates list mapData to store all lines in map.txt
        self.data = []

        # Open map.txt
        with open(filename,'rt') as f:
            for line in f:

                # This is EXTREMELY IMPORTANT. Text files have a "/n" character
                # at the end of each liue to indicate a new line. .strip() removes
                # this character
                self.data.append(line.strip())

        # Takes the length of the first line in map.txt (which is the width)
        self.tilewidth = len(self.data[0])

      # Takes in length of list (which is the length of map)
        self.tileheight = len(self.data)

        # Pixel width of the map
        self.width = self.tilewidth * TILESIZE

        # Pixel height of the map
        self.height = self.tileheight * TILESIZE

# Class to utilize tmxdata in order to render the TiledMap
class TiledMap:
    def __init__(self,filename):
        # Using pytmx with pygame to read the tiled map and render it.
        tm = pytmx.load_pygame(filename,pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self,surface):
        # Aliasing this command because I ceebs typing it over and over again..
        ti = self.tmxdata.get_tile_image_by_gid

        # Going thru each visible layer in the tiledmap
        for layer in self.tmxdata.visible_layers:
            # If the layer is a tiled layer (theres multiple types of layers in Tiled)
            if isinstance(layer, pytmx.TiledTileLayer):
                # Get the coordinates and globalid of each tile in the layer
                for x,y,gid, in layer:
                    # Get tile
                    tile = ti(gid)
                    # If its a tile
                    if tile:
                        # Draw the tile onto the surface (blit it)
                        surface.blit(tile,(x*self.tmxdata.tilewidth,
                                            y*self.tmxdata.tileheight))

    # Make a map by rendering all tiles in proper locations on a surface and return
    # the surface
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

# Controls the camera. Draws the map shifted with an offset.
# Keeps everything consistent, keep track of an offset, how far to the left
# or right do we want to draw the map?
class Camera:
    # Camera does two things, shift drawing rectangles
    # When player moves, update itself to track where the player is.
    def __init__(self,width,height):
        self.camera = pg.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self,rect):
        return rect.move(self.camera.topleft)

    # Shift camera with player sprite.
    def update(self,target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

def gameLoop():
    # Starts an instance of the game
    g = Game()

    # Shows start screen
    g.show_start_screen()

    # Runs loop while g.running is true
    while True:
        g.new()
        g.run()
        # Shows game over screen
        g.show_go_screen()

gameLoop()
