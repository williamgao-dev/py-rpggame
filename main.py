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
    Game art / sprite art:
'''


import pygame as pg ## pygame == pg important..
import random
import time
from settings import *
from os import path
from sprites import *
from tilemap import *

# HUD Function
# Function to draw player health onto screen. Will be called within
# update function
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

        # self.player = Player(self,5,5)
        # Initalize the camera
        self.camera = Camera(self.map.width,self.map.height)
        self.effects_sounds['level_start'].play()
        if DEBUG_LIGHT == "ON":
            self.night = False
        else:
            self.night = True

    # >> Game Loop << Keeps running while self.playing = True
    def run(self):
        # Game Loop
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

        # Alert of debug_mode is off
        if DEBUG_MODE == "OFF":
            print("DEBUG MODE OFF")

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

            # THIS IS AWESOME! Now the bullets have stopping power.,
            mob.vel = vec(0,0)

    # Event handling
    def events(self):

        # Game Loop - Events

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

# Starts an instance of the class Game
g = Game()

# Shows start screen
g.show_start_screen()

# Runs loop while g.running is true
while True:
    g.new()
    g.run()
    g.show_go_screen()
