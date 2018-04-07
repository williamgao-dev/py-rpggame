import pygame as pg
from settings import *
from os import path

# Load assets, gamesounds, spriteimages, sound channels.. etc.
class Map:
    def __init__(self,filename):
        # Assign var gameFolder to root folder

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

    # Shift camera with player sprite.
    def update(self,target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
