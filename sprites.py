import pygame as pg
from settings import *

# Player sprite class
class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        # Initalize an instance of Player in group all_sprites
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        # Sets attributes of class Player, sets a reference to the game class
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    # Function to move the Player object in various directions
    def move(self,dx=0,dy=0):
        if self.wallCollision(dx,dy) == False:
            self.x += dx
            self.y += dy

    # Function to test if next movement of the Player object will collide with an instance of a wall.
    # If the next movement collides, the function will return True.
    def wallCollision(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    # Function that updates the current position of the sprites EVERY frame.
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

# Wall sprite class
class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.walls
        # Initalizes into groups
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # Makes the wall the size of a tile
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE