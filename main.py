# William Gao

import pygame as pg ## pg == pg
import random
import time
from settings import *
from os import path
from sprites import *

class Game:
    def __init__(self):
        # Initialize pygame, pg sounds & game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Starts a timer - used to record events
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100) # Keyboard repeating function, (time key is held, time between repeats)
        # Ensures game remains running until set otherwise
        self.running = True
        self.load_data()

    # Quit function
    def quit(self):
        pg.quit()
        quit()

    # Load assets, gamesounds, spriteimages, sound channels.. etc.
    def load_data(self):
        # Assign var gameFolder to root folder
        gameFolder = path.dirname(__file__)
        # Creates list mapData to store all lines in map.txt
        self.mapData = []
        # Open map.txt
        with open(path.join(gameFolder, 'map.txt'),'rt') as f:
            for line in f:
                self.mapData.append(line)
        # # Debug
        # print (mapData)


    # Called to initalize the game
    def new(self):

        # Initalizes the all_sprites and walls group
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        # Enumerate takes item AND index number <=== IMPORTANT!
        for row, tiles in enumerate(self.mapData):
            for col, tile in enumerate(tiles):
                # If tile is 1, spawn a Wall sprite at the x and y coordinates
                if tile == '1':
                    Wall(self,col,row)
                # If tile is P or p, spawn a Player sprite at the x and y coordinates
                if tile == 'P':
                    self.player = Player(self,col,row)

        # Start a new game
        self.run()

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

    # Event handling
    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                # # Moves the player sprite in x or y values,
                # # triggered by event handling of arrow key keypresses
                # if event.key == pg.K_LEFT:
                #     self.player.move(dx=-1)
                # if event.key == pg.K_RIGHT:
                #     self.player.move(dx=1)
                # if event.key == pg.K_UP:
                #     self.player.move(dy=-1)
                # if event.key == pg.K_DOWN:
                #     self.player.move(dy=1)

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
        self.all_sprites.draw(self.screen)
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
while g.running:
    g.new()
    g.show_go_screen()

# Quit
pg.quit() # Deinitalizes pygame
quit() # Quits python
