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


import pygame as pg ## pg == pg
import random
import time
from settings import *
from os import path
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        # Initialize pygame, pg sounds & game window, etc
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

        # Image folder initalization
        img_folder = path.join(game_folder, 'img')

        # Initalizing the map
        self.map = Map(path.join(game_folder,'map.txt'))

        # Player image variable initalization
        # PLAYER_IMG is specified in the constants in settings.py
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG))

    # Quit function
    def quit(self):
        pg.quit()
        quit()

    # Called to initalize the game
    def new(self):

        # Initalizes the all_sprites and walls group
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        # Enumerate takes item AND index number <=== IMPORTANT!
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):

                # If tile is 1, spawn a Wall sprite at the x and y coordinates
                if tile == '1':
                    Wall(self,col,row)

                # If tile is P, spawn a Player sprite at the x and y coordinates
                if tile == 'P':
                    self.player = Player(self,col,row)

        # Initalize the camera
        self.camera = Camera(self.map.width,self.map.height)


    # >> Game Loop << Keeps running while self.playing = True
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:

            # Delta time, difference in time, in seconds.
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    # Updates all groups every frame per second
    def update(self):

        # Game Loop - Update
        self.all_sprites.update()

        # In every frame, update the camera to match the players offset.
        # THIS IS AMAZING! The camera sprite will follow whatever sprite you command
        # it to follow! In this case, we require the map to move with the camera.
        self.camera.update(self.player)

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
                    self.quit()

    # Function to draw gridmap for game window

    def draw_grid(self):
        # Draws vertical lines
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0),(x,HEIGHT))
        # Draws horizontal lines
        for y in range(0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY,(0,y),(WIDTH,y))

    # Blits and draws all sprites to screen

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image,self.camera.apply(sprite))

        # This will draw a rect around the player hitbox (DEBUG_MODE)
        if DEBUG_MODE == "ON":
            pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def show_start_screen(self):
        # Game splash/start screen
        pass

    def show_go_screen(self):
        # Gameover / continue
        pass

# Starts an instance of the class Game
g = Game()

# Shows start screen
g.show_start_screen()

# Runs loop while g.running is true
while True:
    g.new()
    g.run()
    g.show_go_screen()
