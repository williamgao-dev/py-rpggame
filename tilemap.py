import pygame as pg
from settings import *
from os import path
import pytmx

def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)

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

# Class to render my tiled map made in Tiled
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
